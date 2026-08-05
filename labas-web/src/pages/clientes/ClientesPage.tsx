import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import { useNavigate } from "react-router-dom";
import { clienteService } from "../../services/clienteService";
import { useSnackbar } from "../../hooks/useSnackbar";
import ConfirmDialog from "../../components/shared/ConfirmDialog";
import type { Cliente } from "../../types/cliente";

export default function ClientesPage() {
  const navigate = useNavigate();
  const { showApiError, showSuccess } = useSnackbar();
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [confirmarRemocao, setConfirmarRemocao] = useState<Cliente | null>(null);
  const [removendo, setRemovendo] = useState(false);

  const carregar = useCallback(async () => {
    setLoading(true);
    try {
      const resultado = await clienteService.listar();
      setClientes(resultado);
    } catch (err) {
      showApiError(err);
    } finally {
      setLoading(false);
    }
  }, [showApiError]);

  useEffect(() => {
    void carregar();
  }, [carregar]);

  const handleRemover = useCallback(async () => {
    if (!confirmarRemocao) return;
    setRemovendo(true);
    try {
      await clienteService.remover(confirmarRemocao.codigo);
      showSuccess("Cliente removido.");
      setClientes((prev) => prev.filter((c) => c.codigo !== confirmarRemocao.codigo));
      setConfirmarRemocao(null);
    } catch (err) {
      showApiError(err);
    } finally {
      setRemovendo(false);
    }
  }, [confirmarRemocao, showApiError, showSuccess]);

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
        <Typography variant="h5" fontWeight={700} color="primary">
          Clientes
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate("/clientes/novo")}
        >
          Novo Cliente
        </Button>
      </Box>

      {clientes.length === 0 ? (
        <Alert severity="info">Nenhum cliente cadastrado.</Alert>
      ) : (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Código</TableCell>
                <TableCell>Nome</TableCell>
                <TableCell>Município</TableCell>
                <TableCell>Área</TableCell>
                <TableCell>Telefone</TableCell>
                <TableCell>E-mail</TableCell>
                <TableCell align="right">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {clientes.map((c) => (
                <TableRow key={c.codigo} hover>
                  <TableCell>{c.codigo}</TableCell>
                  <TableCell>{c.nome}</TableCell>
                  <TableCell>{c.municipio ?? "—"}</TableCell>
                  <TableCell>{c.area ?? "—"}</TableCell>
                  <TableCell>{c.telefone ?? "—"}</TableCell>
                  <TableCell>{c.email ?? "—"}</TableCell>
                  <TableCell align="right">
                    <Tooltip title="Editar">
                      <IconButton
                        size="small"
                        onClick={() => navigate(`/clientes/${c.codigo}/editar`)}
                      >
                        <EditIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Remover">
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => setConfirmarRemocao(c)}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
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
        title="Remover cliente"
        message={`Deseja remover permanentemente o cliente "${confirmarRemocao?.nome}" (${confirmarRemocao?.codigo})? Esta ação não pode ser desfeita.`}
        confirmLabel="Remover"
        loading={removendo}
        onConfirm={() => void handleRemover()}
        onCancel={() => setConfirmarRemocao(null)}
      />
    </Box>
  );
}
