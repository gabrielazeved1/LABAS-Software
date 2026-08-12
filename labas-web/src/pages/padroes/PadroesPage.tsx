import { useEffect, useState } from "react";
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  IconButton,
  Stack,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import DownloadIcon from "@mui/icons-material/Download";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import PageHeader from "../../components/shared/PageHeader";
import LoadingOverlay from "../../components/shared/LoadingOverlay";
import ConfirmDialog from "../../components/shared/ConfirmDialog";
import { padraoService } from "../../services/padraoService";
import { useSnackbar } from "../../hooks/useSnackbar";
import type { ConjuntoPadrao, PadraoLaboratorio, PadraoPayload } from "../../types/padroes";

// ─── Campos químicos agrupados para o formulário ──────────────────────────────

const GRUPOS_CAMPOS: { titulo: string; campos: { key: keyof PadraoPayload; label: string }[] }[] = [
  {
    titulo: "pH",
    campos: [
      { key: "ph_agua", label: "pH água" },
      { key: "ph_cacl2", label: "pH CaCl₂" },
      { key: "ph_kcl", label: "pH KCl" },
    ],
  },
  {
    titulo: "Fósforo / Enxofre / Boro",
    campos: [
      { key: "p_m", label: "P-Mehlich (mg/dm³)" },
      { key: "p_r", label: "P-Resina (mg/dm³)" },
      { key: "p_rem", label: "P-rem (mg/L)" },
      { key: "s", label: "S (mg/dm³)" },
      { key: "b", label: "B (mg/dm³)" },
    ],
  },
  {
    titulo: "Bases / Acidez (cmolc/dm³)",
    campos: [
      { key: "k", label: "K" },
      { key: "na", label: "Na" },
      { key: "ca", label: "Ca" },
      { key: "mg", label: "Mg" },
      { key: "al", label: "Al³⁺" },
      { key: "h_al", label: "H+Al" },
    ],
  },
  {
    titulo: "Micronutrientes (mg/dm³)",
    campos: [
      { key: "cu", label: "Cu" },
      { key: "fe", label: "Fe" },
      { key: "mn", label: "Mn" },
      { key: "zn", label: "Zn" },
    ],
  },
  {
    titulo: "Matéria Orgânica / C-org",
    campos: [
      { key: "mo", label: "MO (dag/kg)" },
      { key: "c_org", label: "C-org (dag/kg)" },
    ],
  },
  {
    titulo: "Calculados",
    campos: [
      { key: "sb", label: "SB (cmolc/dm³)" },
      { key: "t", label: "t — CTC efetiva" },
      { key: "T_maiusculo", label: "T — CTC pH 7,0" },
      { key: "V", label: "V%" },
      { key: "m", label: "m%" },
      { key: "ca_mg", label: "Ca/Mg" },
      { key: "ca_k", label: "Ca/K" },
      { key: "mg_k", label: "Mg/K" },
    ],
  },
];

// ─── Formulário de uma linha de padrão ───────────────────────────────────────

function FormPadrao({
  padrao,
  conjuntoId,
  onSalvo,
}: {
  padrao: PadraoLaboratorio;
  conjuntoId: number;
  onSalvo: () => void;
}) {
  const { showSuccess, showApiError } = useSnackbar();
  const [salvando, setSalvando] = useState(false);
  const [valores, setValores] = useState<PadraoPayload>(() => {
    const p = padrao as Record<string, unknown>;
    return Object.fromEntries(
      Object.keys(padrao)
        .filter((k) => !["id", "tipo", "tipo_display"].includes(k))
        .map((k) => [k, p[k] ?? ""]),
    ) as unknown as PadraoPayload;
  });

  const handleChange = (key: keyof PadraoPayload, val: string) => {
    setValores((prev) => ({ ...prev, [key]: val === "" ? null : Number(val) }));
  };

  const handleSalvar = async () => {
    setSalvando(true);
    try {
      await padraoService.atualizarPadrao(conjuntoId, padrao.tipo, valores);
      showSuccess(`${padrao.tipo_display} salvo!`);
      onSalvo();
    } catch (err) {
      showApiError(err);
    } finally {
      setSalvando(false);
    }
  };

  return (
    <Box>
      {GRUPOS_CAMPOS.map((grupo) => (
        <Box key={grupo.titulo} mb={2}>
          <Typography variant="caption" color="text.secondary" display="block" mb={1}>
            {grupo.titulo}
          </Typography>
          <Grid container spacing={1}>
            {grupo.campos.map(({ key, label }) => (
              <Grid key={key} size={{ xs: 6, sm: 4, md: 3 }}>
                <TextField
                  label={label}
                  size="small"
                  fullWidth
                  type="number"
                  inputProps={{ step: "any" }}
                  value={valores[key] ?? ""}
                  onChange={(e) => handleChange(key, e.target.value)}
                  placeholder="*"
                />
              </Grid>
            ))}
          </Grid>
        </Box>
      ))}
      <Button
        variant="contained"
        size="small"
        onClick={() => void handleSalvar()}
        disabled={salvando}
        startIcon={salvando ? <CircularProgress size={16} color="inherit" /> : undefined}
      >
        {salvando ? "Salvando..." : "Salvar"}
      </Button>
    </Box>
  );
}

// ─── Componente principal ─────────────────────────────────────────────────────

export default function PadroesPage() {
  const { showSuccess, showApiError } = useSnackbar();
  const [conjuntos, setConjuntos] = useState<ConjuntoPadrao[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [baixandoPdf, setBaixandoPdf] = useState<number | null>(null);

  // Dialog: novo conjunto
  const [dialogNovoAberto, setDialogNovoAberto] = useState(false);
  const [nomeNovo, setNomeNovo] = useState("");
  const [criando, setCriando] = useState(false);

  // Dialog: editar nome
  const [editando, setEditando] = useState<ConjuntoPadrao | null>(null);
  const [nomeEditado, setNomeEditado] = useState("");
  const [salvandoNome, setSalvandoNome] = useState(false);

  // Confirmação de remoção
  const [confirmarRemocao, setConfirmarRemocao] = useState<ConjuntoPadrao | null>(null);

  const carregar = async () => {
    try {
      const data = await padraoService.listar();
      setConjuntos(data);
    } catch (err) {
      showApiError(err);
    } finally {
      setCarregando(false);
    }
  };

  useEffect(() => {
    void carregar();
  }, []);

  const handleAtivar = async (id: number) => {
    try {
      await padraoService.ativar(id);
      showSuccess("Conjunto ativado!");
      void carregar();
    } catch (err) {
      showApiError(err);
    }
  };

  const handleDesativar = async (id: number) => {
    try {
      await padraoService.desativar(id);
      showSuccess("Conjunto desativado.");
      void carregar();
    } catch (err) {
      showApiError(err);
    }
  };

  const handleRemover = async () => {
    if (!confirmarRemocao) return;
    try {
      await padraoService.remover(confirmarRemocao.id);
      showSuccess("Conjunto removido.");
      setConfirmarRemocao(null);
      void carregar();
    } catch (err) {
      showApiError(err);
      setConfirmarRemocao(null);
    }
  };

  const handleBaixarPdf = async (id: number) => {
    setBaixandoPdf(id);
    try {
      const blob = await padraoService.baixarPdf(id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const nome = conjuntos.find((c) => c.id === id)?.nome ?? "padroes";
      a.download = `padroes-${nome.replace(/\s+/g, "-")}.pdf`;
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      showApiError(err);
    } finally {
      setBaixandoPdf(null);
    }
  };

  const handleCriar = async () => {
    if (!nomeNovo.trim()) return;
    setCriando(true);
    try {
      await padraoService.criar(nomeNovo.trim());
      showSuccess("Conjunto criado!");
      setNomeNovo("");
      setDialogNovoAberto(false);
      void carregar();
    } catch (err) {
      showApiError(err);
    } finally {
      setCriando(false);
    }
  };

  const handleAbrirEdicao = (conjunto: ConjuntoPadrao) => {
    setEditando(conjunto);
    setNomeEditado(conjunto.nome);
  };

  const handleSalvarNome = async () => {
    if (!editando || !nomeEditado.trim()) return;
    setSalvandoNome(true);
    try {
      await padraoService.renomear(editando.id, nomeEditado.trim());
      showSuccess("Nome atualizado!");
      setEditando(null);
      void carregar();
    } catch (err) {
      showApiError(err);
    } finally {
      setSalvandoNome(false);
    }
  };

  if (carregando) {
    return (
      <Box display="flex" justifyContent="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <LoadingOverlay open={baixandoPdf !== null} message="Gerando PDF..." />

      <PageHeader
        title="Conjuntos de Padrões"
        subtitle="Valores de referência utilizados nas linhas iniciais do PDF de laudo"
      />

      <Box mb={3}>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setDialogNovoAberto(true)}
        >
          Novo Conjunto
        </Button>
      </Box>

      {conjuntos.length === 0 && (
        <Alert severity="info">
          Nenhum conjunto cadastrado. Crie o primeiro para definir os valores de referência.
        </Alert>
      )}

      {conjuntos.map((conjunto) => (
        <Accordion key={conjunto.id} sx={{ mb: 1 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Stack direction="row" alignItems="center" spacing={1} flexGrow={1} pr={1}>
              <Typography fontWeight={600}>{conjunto.nome}</Typography>

              {conjunto.ativo && (
                <Chip
                  label="Ativo"
                  color="success"
                  size="small"
                  icon={<CheckCircleIcon />}
                />
              )}

              <Box flexGrow={1} />

              {/* Gerar PDF */}
              <Tooltip title="Gerar PDF deste conjunto">
                <span>
                  <IconButton
                    size="small"
                    onClick={(e) => { e.stopPropagation(); void handleBaixarPdf(conjunto.id); }}
                    disabled={baixandoPdf === conjunto.id}
                  >
                    <DownloadIcon fontSize="small" />
                  </IconButton>
                </span>
              </Tooltip>

              {/* Editar nome */}
              <Tooltip title="Editar nome">
                <IconButton
                  size="small"
                  onClick={(e) => { e.stopPropagation(); handleAbrirEdicao(conjunto); }}
                >
                  <EditIcon fontSize="small" />
                </IconButton>
              </Tooltip>

              {/* Ativar / Desativar */}
              {conjunto.ativo ? (
                <Tooltip title="Desativar este conjunto">
                  <Button
                    size="small"
                    variant="outlined"
                    color="warning"
                    onClick={(e) => { e.stopPropagation(); void handleDesativar(conjunto.id); }}
                  >
                    Desativar
                  </Button>
                </Tooltip>
              ) : (
                <Tooltip title="Tornar este conjunto o ativo">
                  <Button
                    size="small"
                    variant="outlined"
                    color="success"
                    onClick={(e) => { e.stopPropagation(); void handleAtivar(conjunto.id); }}
                  >
                    Ativar
                  </Button>
                </Tooltip>
              )}

              {/* Remover */}
              <Tooltip title="Remover conjunto">
                <IconButton
                  size="small"
                  color="error"
                  onClick={(e) => { e.stopPropagation(); setConfirmarRemocao(conjunto); }}
                >
                  <DeleteIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </Stack>
          </AccordionSummary>

          <AccordionDetails>
            {conjunto.padroes.map((padrao, idx) => (
              <Box key={padrao.tipo}>
                {idx > 0 && <Divider sx={{ my: 2 }} />}
                <Typography variant="subtitle2" fontWeight={700} mb={2}>
                  {padrao.tipo_display}
                </Typography>
                <FormPadrao
                  padrao={padrao}
                  conjuntoId={conjunto.id}
                  onSalvo={() => void carregar()}
                />
              </Box>
            ))}
          </AccordionDetails>
        </Accordion>
      ))}

      {/* ── Dialog: criar conjunto ──────────────────────────────────────────── */}
      <Dialog
        open={dialogNovoAberto}
        onClose={() => setDialogNovoAberto(false)}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>Novo conjunto de padrões</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            label="Nome do conjunto"
            placeholder="Ex: Padrão Jun/2026"
            value={nomeNovo}
            onChange={(e) => setNomeNovo(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") void handleCriar(); }}
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogNovoAberto(false)}>Cancelar</Button>
          <Button
            variant="contained"
            disabled={!nomeNovo.trim() || criando}
            onClick={() => void handleCriar()}
          >
            {criando ? "Criando..." : "Criar"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* ── Dialog: editar nome ─────────────────────────────────────────────── */}
      <Dialog
        open={!!editando}
        onClose={() => setEditando(null)}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>Editar nome</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            label="Nome do conjunto"
            value={nomeEditado}
            onChange={(e) => setNomeEditado(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") void handleSalvarNome(); }}
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditando(null)}>Cancelar</Button>
          <Button
            variant="contained"
            disabled={!nomeEditado.trim() || salvandoNome}
            onClick={() => void handleSalvarNome()}
          >
            {salvandoNome ? "Salvando..." : "Salvar"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* ── Confirmação de remoção ──────────────────────────────────────────── */}
      <ConfirmDialog
        open={!!confirmarRemocao}
        title="Remover conjunto"
        message={
          confirmarRemocao?.ativo
            ? `"${confirmarRemocao?.nome}" é o conjunto ativo. Ao remover, nenhum conjunto estará ativo. Deseja continuar?`
            : `Deseja remover permanentemente o conjunto "${confirmarRemocao?.nome}"? Esta ação não pode ser desfeita.`
        }
        confirmLabel="Remover"
        onCancel={() => setConfirmarRemocao(null)}
        onConfirm={() => void handleRemover()}
      />
    </Box>
  );
}
