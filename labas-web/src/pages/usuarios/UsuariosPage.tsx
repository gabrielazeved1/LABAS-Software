import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import { z } from "zod";
import { useSnackbar } from "../../hooks/useSnackbar";
import { usuarioService, type Tecnico, type TecnicoCriarPayload } from "../../services/usuarioService";
import { useAuth } from "../../hooks/useAuth";
import ConfirmDialog from "../../components/shared/ConfirmDialog";

const tecnicoSchema = z
  .object({
    nome: z.string().min(1, "Nome é obrigatório"),
    username: z.string().min(3, "Mínimo de 3 caracteres"),
    email: z.string().email("E-mail inválido"),
    password: z.string().min(8, "Mínimo de 8 caracteres"),
    password2: z.string(),
  })
  .refine((d) => d.password === d.password2, {
    message: "As senhas não coincidem",
    path: ["password2"],
  });

const FORM_VAZIO: TecnicoCriarPayload & { password2: string } = {
  username: "",
  email: "",
  nome: "",
  password: "",
  password2: "",
};

export default function UsuariosPage() {
  const { user: usuarioLogado } = useAuth();
  const { showApiError, showSuccess, showError } = useSnackbar();

  const [tecnicos, setTecnicos] = useState<Tecnico[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogAberto, setDialogAberto] = useState(false);
  const [salvando, setSalvando] = useState(false);
  const [form, setForm] = useState(FORM_VAZIO);
  const [erros, setErros] = useState<Partial<typeof FORM_VAZIO>>({});
  const [confirmarRemocao, setConfirmarRemocao] = useState<Tecnico | null>(null);

  const carregar = useCallback(async () => {
    setLoading(true);
    try {
      const lista = await usuarioService.listar();
      setTecnicos(lista);
    } catch (err) {
      showApiError(err);
    } finally {
      setLoading(false);
    }
  }, [showApiError]);

  useEffect(() => {
    void carregar();
  }, [carregar]);

  const abrirDialog = () => {
    setForm(FORM_VAZIO);
    setErros({});
    setDialogAberto(true);
  };

  const fecharDialog = () => {
    if (salvando) return;
    setDialogAberto(false);
  };

  const validar = (): boolean => {
    const resultado = tecnicoSchema.safeParse(form);
    if (resultado.success) {
      setErros({});
      return true;
    }
    const novosErros: Partial<typeof FORM_VAZIO> = {};
    for (const issue of resultado.error.issues) {
      const campo = issue.path[0] as keyof typeof FORM_VAZIO;
      if (campo && !novosErros[campo]) novosErros[campo] = issue.message;
    }
    setErros(novosErros);
    return false;
  };

  const handleSalvar = async () => {
    if (!validar()) return;
    setSalvando(true);
    try {
      const novo = await usuarioService.criar({
        username: form.username,
        email: form.email,
        nome: form.nome,
        password: form.password,
      });
      setTecnicos((prev) => [...prev, novo]);
      showSuccess("Técnico cadastrado com sucesso.");
      setDialogAberto(false);
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: Record<string, string[]> } };
      const data = axiosErr?.response?.data;
      if (data) {
        const msg = Object.values(data).flat()[0];
        showError(msg ?? "Erro ao cadastrar técnico.");
      } else {
        showApiError(err);
      }
    } finally {
      setSalvando(false);
    }
  };

  const handleRemover = useCallback(
    (tecnico: Tecnico) => {
      if (tecnico.id === usuarioLogado?.id) {
        showError("Você não pode remover sua própria conta.");
        return;
      }
      setConfirmarRemocao(tecnico);
    },
    [usuarioLogado, showError],
  );

  const confirmarRemoverTecnico = useCallback(async () => {
    if (!confirmarRemocao) return;
    try {
      await usuarioService.remover(confirmarRemocao.id);
      setTecnicos((prev) => prev.filter((t) => t.id !== confirmarRemocao.id));
      showSuccess("Técnico removido.");
    } catch (err) {
      showApiError(err);
    } finally {
      setConfirmarRemocao(null);
    }
  }, [confirmarRemocao, showApiError, showSuccess]);

  const campo = (
    field: keyof typeof FORM_VAZIO,
    label: string,
    type = "text",
  ) => (
    <TextField
      label={label}
      type={type}
      fullWidth
      size="small"
      value={form[field]}
      onChange={(e) => setForm((p) => ({ ...p, [field]: e.target.value }))}
      error={!!erros[field]}
      helperText={erros[field]}
      disabled={salvando}
      autoComplete="off"
    />
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Box>
          <Typography variant="h5" fontWeight={700} color="primary">
            Usuários
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Técnicos com acesso ao sistema
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<AddIcon />} onClick={abrirDialog}>
          Novo Técnico
        </Button>
      </Box>

      {tecnicos.length === 0 ? (
        <Alert severity="info">Nenhum técnico cadastrado.</Alert>
      ) : (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Usuário</TableCell>
                <TableCell>Nome</TableCell>
                <TableCell>E-mail</TableCell>
                <TableCell>Cadastrado em</TableCell>
                <TableCell align="right">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {tecnicos.map((t) => (
                <TableRow
                  key={t.id}
                  hover
                  sx={t.id === usuarioLogado?.id ? { bgcolor: "action.hover" } : {}}
                >
                  <TableCell>
                    <Typography variant="body2" fontWeight={600}>
                      {t.username}
                    </Typography>
                    {t.id === usuarioLogado?.id && (
                      <Typography variant="caption" color="text.secondary">
                        (você)
                      </Typography>
                    )}
                  </TableCell>
                  <TableCell>{t.nome}</TableCell>
                  <TableCell>{t.email}</TableCell>
                  <TableCell>
                    {new Date(t.date_joined).toLocaleDateString("pt-BR")}
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title={t.id === usuarioLogado?.id ? "Não é possível remover sua própria conta" : "Remover"}>
                      <span>
                        <IconButton
                          size="small"
                          color="error"
                          disabled={t.id === usuarioLogado?.id}
                          onClick={() => handleRemover(t)}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </span>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <ConfirmDialog
        open={confirmarRemocao !== null}
        title="Remover técnico"
        message={`Deseja remover permanentemente o técnico "${confirmarRemocao?.username}"? Esta ação não pode ser desfeita.`}
        confirmLabel="Remover"
        onConfirm={confirmarRemoverTecnico}
        onCancel={() => setConfirmarRemocao(null)}
      />

      <Dialog open={dialogAberto} onClose={fecharDialog} maxWidth="xs" fullWidth>
        <DialogTitle>Novo Técnico</DialogTitle>
        <DialogContent>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2, pt: 1 }}>
            {campo("nome", "Nome completo")}
            {campo("username", "Usuário")}
            {campo("email", "E-mail", "email")}
            {campo("password", "Senha", "password")}
            {campo("password2", "Confirmar senha", "password")}
          </Box>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={fecharDialog} disabled={salvando}>
            Cancelar
          </Button>
          <Button
            variant="contained"
            onClick={handleSalvar}
            disabled={salvando}
          >
            {salvando ? <CircularProgress size={20} color="inherit" /> : "Cadastrar"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
