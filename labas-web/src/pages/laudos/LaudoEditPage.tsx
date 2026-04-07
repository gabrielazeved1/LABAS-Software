import { useEffect, useMemo, useState } from "react";
import { Controller } from "react-hook-form";
import {
  Alert,
  Autocomplete,
  Box,
  Button,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  IconButton,
  Paper,
  Stack,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import type { GridColDef } from "@mui/x-data-grid";
import AddIcon from "@mui/icons-material/Add";
import BiotechIcon from "@mui/icons-material/Biotech";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import ScienceIcon from "@mui/icons-material/Science";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { Link as RouterLink, useNavigate, useParams } from "react-router-dom";
import PageHeader from "../../components/shared/PageHeader";
import LoadingOverlay from "../../components/shared/LoadingOverlay";
import ConfirmDialog from "../../components/shared/ConfirmDialog";
import DialogCorrecaoAnalise from "../../components/shared/DialogCorrecaoAnalise";
import { useLaudoEditForm } from "../../hooks/useLaudoEditForm";
import { useAnalises } from "../../hooks/useAnalises";
import { useClientes } from "../../hooks/useClientes";
import { laudoService } from "../../services/laudoService";
import { useSnackbar } from "../../hooks/useSnackbar";
import type { Cliente } from "../../types/cliente";
import type { Laudo, AnaliseSolo } from "../../types/analise";

export default function LaudoEditPage() {
  const { id: idParam } = useParams<{ id: string }>();
  const laudoId = idParam ? parseInt(idParam, 10) : undefined;
  const navigate = useNavigate();
  const { showApiError } = useSnackbar();

  const [laudo, setLaudo] = useState<Laudo | undefined>();
  const [buscando, setBuscando] = useState(true);
  const [erroFetch, setErroFetch] = useState(false);
  const [confirmarRemocao, setConfirmarRemocao] = useState<AnaliseSolo | null>(
    null,
  );
  const [analiseCorrecao, setAnaliseCorrecao] = useState<AnaliseSolo | null>(
    null,
  );

  const [clienteSelecionado, setClienteSelecionado] = useState<Cliente | null>(
    null,
  );
  const [clienteInput, setClienteInput] = useState("");

  const { clientes, loading: clientesLoading, buscar, limpar } = useClientes();
  const { form, submitting, onSubmit } = useLaudoEditForm(laudo);
  const {
    analises,
    loading: analisesLoading,
    salvando,
    editando,
    removendo,
    remover,
    toggleAtivo,
    criar,
    editar,
  } = useAnalises(laudoId);

  // ── Dialog "Nova Amostra" ─────────────────────────────────────────────────
  const [dialogAberto, setDialogAberto] = useState(false);
  const [nLabNovo, setNLabNovo] = useState("");
  const [referenciaNova, setReferenciaNova] = useState("");
  const [dataEntradaNova, setDataEntradaNova] = useState("");
  const [erroNLab, setErroNLab] = useState("");

  // ── Dialog "Editar Amostra" ───────────────────────────────────────────────
  const [editandoAmostra, setEditandoAmostra] = useState<AnaliseSolo | null>(
    null,
  );
  const [nLabEdit, setNLabEdit] = useState("");
  const [referenciaEdit, setReferenciaEdit] = useState("");
  const [dataEntradaEdit, setDataEntradaEdit] = useState("");
  const [erroEdit, setErroEdit] = useState("");

  const abrirDialogEdicao = (analise: AnaliseSolo) => {
    setNLabEdit(analise.n_lab);
    setReferenciaEdit(analise.referencia ?? "");
    setDataEntradaEdit(analise.data_entrada);
    setErroEdit("");
    setEditandoAmostra(analise);
  };

  const handleEditarAmostra = async () => {
    if (!/^\d{4}\/\d{3}$/.test(nLabEdit.trim())) {
      setErroEdit("Formato inválido. Use AAAA/NNN (ex: 2026/001)");
      return;
    }
    if (!dataEntradaEdit) {
      setErroEdit("Data de entrada obrigatória");
      return;
    }
    if (!editandoAmostra) return;
    await editar(editandoAmostra.id, {
      n_lab: nLabEdit.trim(),
      referencia: referenciaEdit || null,
      data_entrada: dataEntradaEdit,
    });
    setEditandoAmostra(null);
  };

  const abrirDialog = () => {
    setNLabNovo("");
    setReferenciaNova("");
    setDataEntradaNova("");
    setErroNLab("");
    setDialogAberto(true);
  };

  const handleCriarAmostra = async () => {
    if (!/^\d{4}\/\d{3}$/.test(nLabNovo.trim())) {
      setErroNLab("Formato inválido. Use AAAA/NNN (ex: 2026/001)");
      return;
    }
    if (!dataEntradaNova) {
      setErroNLab("Data de entrada obrigatória");
      return;
    }
    await criar({
      n_lab: nLabNovo.trim(),
      referencia: referenciaNova || null,
      data_entrada: dataEntradaNova,
      ativo: true,
    });
    setDialogAberto(false);
  };

  useEffect(() => {
    if (!laudoId) {
      navigate("/laudos");
      return;
    }
    laudoService
      .buscar(laudoId)
      .then((data) => {
        setLaudo(data);
        setClienteSelecionado(data.cliente);
        setClienteInput(`${data.cliente.codigo} — ${data.cliente.nome}`);
      })
      .catch((err) => {
        showApiError(err);
        setErroFetch(true);
      })
      .finally(() => setBuscando(false));
  }, [laudoId, navigate, showApiError]);

  const clientesOpcoes = useMemo(() => {
    if (!clienteSelecionado) return clientes;
    if (clientes.some((c) => c.codigo === clienteSelecionado.codigo))
      return clientes;
    return [clienteSelecionado, ...clientes];
  }, [clientes, clienteSelecionado]);

  const handleClienteInput = (_: React.SyntheticEvent, value: string) => {
    setClienteInput(value);
    if (value.trim().length === 0) {
      if (clienteSelecionado) {
        setClienteSelecionado(null);
        form.setValue("cliente_codigo", "", {
          shouldDirty: true,
          shouldValidate: true,
        });
      }
      limpar();
      return;
    }
    if (value.trim().length < 2) {
      limpar();
      return;
    }
    buscar(value);
  };

  const colunas: GridColDef<AnaliseSolo>[] = [
    { field: "n_lab", headerName: "N° Lab", width: 110 },
    { field: "referencia", headerName: "Referência", flex: 1 },
    { field: "data_entrada", headerName: "Entrada", width: 110 },
    {
      field: "ativo",
      headerName: "Ativo",
      width: 90,
      renderCell: ({ row }) => (
        <Chip
          size="small"
          label={row.ativo ? "Sim" : "Não"}
          color={row.ativo ? "success" : "default"}
        />
      ),
    },
    {
      field: "sb",
      headerName: "SB",
      width: 80,
      valueFormatter: (value: number | null) => value ?? "—",
    },
    {
      field: "ctc",
      headerName: "CTC",
      width: 80,
      valueFormatter: (value: number | null) => value ?? "—",
    },
    {
      field: "v",
      headerName: "V%",
      width: 80,
      valueFormatter: (value: number | null) =>
        value != null ? `${value}%` : "—",
    },
    {
      field: "acoes",
      headerName: "Ações",
      width: 100,
      sortable: false,
      renderCell: ({ row }) => (
        <Stack direction="row" spacing={0.5}>
          <Tooltip title="Editar ficha da amostra">
            <IconButton
              size="small"
              disabled={editando === row.id}
              onClick={() => abrirDialogEdicao(row)}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Corrigir leituras / granulometria">
            <IconButton
              size="small"
              color="secondary"
              onClick={() => setAnaliseCorrecao(row)}
            >
              <ScienceIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title={row.ativo ? "Desativar (oculta do PDF)" : "Ativar"}>
            <IconButton
              size="small"
              onClick={() => void toggleAtivo(row.id, !row.ativo)}
            >
              {row.ativo ? (
                <VisibilityOffIcon fontSize="small" />
              ) : (
                <VisibilityIcon fontSize="small" />
              )}
            </IconButton>
          </Tooltip>
          <Tooltip title="Remover análise">
            <IconButton
              size="small"
              color="error"
              disabled={removendo === row.id}
              onClick={() => setConfirmarRemocao(row)}
            >
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Stack>
      ),
    },
  ];

  if (buscando) {
    return (
      <Box display="flex" justifyContent="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  if (erroFetch || !laudo) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>
          Não foi possível carregar o laudo.
        </Alert>
        <Button variant="outlined" component={RouterLink} to="/laudos">
          Voltar para laudos
        </Button>
      </Box>
    );
  }

  return (
    <Box component="form" onSubmit={onSubmit} noValidate>
      <LoadingOverlay open={submitting} message="Salvando alterações..." />

      <PageHeader
        title={`Editar Laudo ${laudo.codigo_laudo}`}
        subtitle="Atualize o cabeçalho e gerencie as análises vinculadas"
        actions={
          <Button
            variant="contained"
            startIcon={<BiotechIcon />}
            component={RouterLink}
            to="/entrada-lote"
          >
            Ir para Amostras
          </Button>
        }
      />

      {/* ── Cabeçalho ──────────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Dados do laudo
        </Typography>
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, sm: 4 }}>
            <TextField
              fullWidth
              size="small"
              label="Código"
              value={laudo.codigo_laudo}
              slotProps={{ input: { readOnly: true } }}
              disabled
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 4 }}>
            <TextField
              fullWidth
              size="small"
              label="Data de Entrada *"
              type="date"
              slotProps={{ inputLabel: { shrink: true } }}
              error={!!form.formState.errors.data_emissao}
              helperText={form.formState.errors.data_emissao?.message}
              disabled={submitting}
              {...form.register("data_emissao")}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 4 }}>
            <TextField
              fullWidth
              size="small"
              label="Data de Saída"
              type="date"
              slotProps={{ inputLabel: { shrink: true } }}
              error={!!form.formState.errors.data_saida}
              helperText={form.formState.errors.data_saida?.message}
              disabled={submitting}
              {...form.register("data_saida")}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 8 }}>
            <Controller
              control={form.control}
              name="cliente_codigo"
              render={({ field, fieldState }) => (
                <Autocomplete
                  options={clientesOpcoes}
                  value={clienteSelecionado}
                  inputValue={clienteInput}
                  onInputChange={handleClienteInput}
                  onChange={(_, value) => {
                    setClienteSelecionado(value);
                    field.onChange(value?.codigo ?? "");
                  }}
                  onBlur={field.onBlur}
                  loading={clientesLoading}
                  noOptionsText={
                    clienteInput.length < 2
                      ? "Digite pelo menos 2 caracteres"
                      : "Nenhum cliente encontrado"
                  }
                  getOptionLabel={(option) =>
                    `${option.codigo} — ${option.nome}`
                  }
                  isOptionEqualToValue={(option, value) =>
                    option.codigo === value.codigo
                  }
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Cliente *"
                      size="small"
                      error={!!fieldState.error}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />
              )}
            />
          </Grid>

          <Grid size={12}>
            <TextField
              fullWidth
              size="small"
              label="Observações"
              multiline
              rows={2}
              disabled={submitting}
              {...form.register("observacoes")}
            />
          </Grid>
        </Grid>
      </Paper>

      {/* ── Análises vinculadas ────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          mb={2}
        >
          <Typography variant="subtitle1" fontWeight={700}>
            Amostras ({analises.length})
          </Typography>
          <Button
            size="small"
            variant="outlined"
            startIcon={<AddIcon />}
            onClick={abrirDialog}
          >
            Nova Amostra
          </Button>
        </Stack>
        <DataGrid
          rows={analises}
          columns={colunas}
          loading={analisesLoading}
          autoHeight
          disableRowSelectionOnClick
          pageSizeOptions={[10, 25, 50]}
          initialState={{ pagination: { paginationModel: { pageSize: 10 } } }}
          sx={{
            "& .MuiDataGrid-cell": { alignItems: "center", display: "flex" },
          }}
        />
      </Paper>

      <Stack direction={{ xs: "column", sm: "row" }} spacing={2} mb={4}>
        <Button variant="outlined" component={RouterLink} to="/laudos">
          Voltar
        </Button>
        <Button type="submit" variant="contained" disabled={submitting}>
          {submitting ? "Salvando..." : "Salvar alterações"}
        </Button>
      </Stack>

      <ConfirmDialog
        open={confirmarRemocao !== null}
        title="Remover análise"
        message={`Deseja remover permanentemente a análise ${confirmarRemocao?.n_lab}?`}
        confirmLabel="Remover"
        loading={removendo !== null}
        onConfirm={async () => {
          if (confirmarRemocao) {
            await remover(confirmarRemocao.id);
            setConfirmarRemocao(null);
          }
        }}
        onCancel={() => setConfirmarRemocao(null)}
      />

      {/* ── Dialog Editar Amostra ───────────────────────────────────────── */}
      <Dialog
        open={editandoAmostra !== null}
        onClose={() => setEditandoAmostra(null)}
        fullWidth
        maxWidth="xs"
      >
        <DialogTitle>Editar Amostra</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            <TextField
              label="N° Lab *"
              placeholder="2026/001"
              size="small"
              fullWidth
              value={nLabEdit}
              onChange={(e) => {
                setNLabEdit(e.target.value);
                setErroEdit("");
              }}
              error={!!erroEdit && erroEdit.includes("Formato")}
              helperText={
                erroEdit.includes("Formato") ? erroEdit : "Formato: AAAA/NNN"
              }
              inputProps={{ maxLength: 8 }}
            />
            <TextField
              label="Referência"
              placeholder="Identificação do produtor / talhão"
              size="small"
              fullWidth
              value={referenciaEdit}
              onChange={(e) => setReferenciaEdit(e.target.value)}
            />
            <TextField
              label="Data de entrada *"
              type="date"
              size="small"
              fullWidth
              value={dataEntradaEdit}
              onChange={(e) => {
                setDataEntradaEdit(e.target.value);
                setErroEdit("");
              }}
              slotProps={{ inputLabel: { shrink: true } }}
              error={!!erroEdit && erroEdit.includes("Data")}
              helperText={erroEdit.includes("Data") ? erroEdit : undefined}
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditandoAmostra(null)}>Cancelar</Button>
          <Button
            variant="contained"
            disabled={editando !== null}
            onClick={() => void handleEditarAmostra()}
          >
            {editando !== null ? "Salvando..." : "Salvar"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* ── Dialog Nova Amostra ─────────────────────────────────────────── */}
      <Dialog
        open={dialogAberto}
        onClose={() => setDialogAberto(false)}
        fullWidth
        maxWidth="xs"
      >
        <DialogTitle>Nova Amostra</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            <TextField
              label="N° Lab *"
              placeholder="2026/001"
              size="small"
              fullWidth
              value={nLabNovo}
              onChange={(e) => {
                setNLabNovo(e.target.value);
                setErroNLab("");
              }}
              error={!!erroNLab && erroNLab.includes("Formato")}
              helperText={
                erroNLab.includes("Formato") ? erroNLab : "Formato: AAAA/NNN"
              }
              inputProps={{ maxLength: 8 }}
            />
            <TextField
              label="Referência"
              placeholder="Identificação do produtor / talhão"
              size="small"
              fullWidth
              value={referenciaNova}
              onChange={(e) => setReferenciaNova(e.target.value)}
            />
            <TextField
              label="Data de entrada *"
              type="date"
              size="small"
              fullWidth
              value={dataEntradaNova}
              onChange={(e) => {
                setDataEntradaNova(e.target.value);
                setErroNLab("");
              }}
              slotProps={{ inputLabel: { shrink: true } }}
              error={!!erroNLab && erroNLab.includes("Data")}
              helperText={erroNLab.includes("Data") ? erroNLab : undefined}
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogAberto(false)}>Cancelar</Button>
          <Button
            variant="contained"
            disabled={salvando}
            onClick={() => void handleCriarAmostra()}
          >
            {salvando ? "Salvando..." : "Adicionar"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* ── Dialog Correção de Análise ──────────────────────────────────── */}
      {analiseCorrecao && laudoId && (
        <DialogCorrecaoAnalise
          open={analiseCorrecao !== null}
          laudoId={laudoId}
          analiseId={analiseCorrecao.id}
          onClose={() => setAnaliseCorrecao(null)}
        />
      )}
    </Box>
  );
}
