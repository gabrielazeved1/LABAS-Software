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
import type { Cliente } from "../../types/cliente";

export default function ClientesPage() {
  const navigate = useNavigate();
  const { showApiError, showSuccess } = useSnackbar();
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);

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

  const handleRemover = useCallback(
    async (codigo: string) => {
      if (!window.confirm(`Remover cliente ${codigo}?`)) return;
      try {
        await clienteService.remover(codigo);
        showSuccess("Cliente removido.");
        setClientes((prev) => prev.filter((c) => c.codigo !== codigo));
      } catch (err) {
        showApiError(err);
      }
    },
    [showApiError, showSuccess],
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
                <TableCell>Contato</TableCell>
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
                  <TableCell>{c.contato ?? "—"}</TableCell>
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
                        onClick={() => handleRemover(c.codigo)}
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
    </Box>
  );
}
