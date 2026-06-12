import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  IconButton,
  InputAdornment,
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
import EditIcon from "@mui/icons-material/Edit";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import VisibilityIcon from "@mui/icons-material/Visibility";
import SearchIcon from "@mui/icons-material/Search";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { useLaudos } from "../../hooks/useLaudos";
import ConfirmDialog from "../../components/shared/ConfirmDialog";
import PageHeader from "../../components/shared/PageHeader";

export default function LaudosPage() {
  const navigate = useNavigate();
  const { isStaff } = useAuth();
  const { laudos, loading, deletando, baixarPdf, excluir } = useLaudos();

  const [filtro, setFiltro] = useState("");
  const [confirmarExclusao, setConfirmarExclusao] = useState<number | null>(
    null,
  );

  const laudosFiltrados = laudos.filter((l) => {
    const termo = filtro.toLowerCase();
    return (
      l.codigo_laudo.toLowerCase().includes(termo) ||
      l.cliente.nome.toLowerCase().includes(termo) ||
      l.cliente.codigo.toLowerCase().includes(termo)
    );
  });

  const laudoParaExcluir = laudos.find((l) => l.id === confirmarExclusao);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <PageHeader
        title="Laudos"
        subtitle={
          isStaff ? "Todos os laudos do laboratório" : "Seus laudos de análise"
        }
      />

      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
          gap: 2,
          flexWrap: "wrap",
        }}
      >
        <TextField
          size="small"
          placeholder="Filtrar por código ou cliente..."
          value={filtro}
          onChange={(e) => setFiltro(e.target.value)}
          sx={{ minWidth: 280 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            },
          }}
        />

        {isStaff && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate("/laudos/novo")}
          >
            Novo Laudo
          </Button>
        )}
      </Box>

      {laudosFiltrados.length === 0 ? (
        <Alert severity="info">
          {filtro
            ? "Nenhum laudo encontrado para este filtro."
            : "Nenhum laudo cadastrado."}
        </Alert>
      ) : (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Código</TableCell>
                <TableCell>Cliente</TableCell>
                <TableCell>Data Emissão</TableCell>
                <TableCell align="right">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {laudosFiltrados.map((laudo) => (
                <TableRow key={laudo.id} hover>
                  <TableCell>
                    <Typography variant="body2" fontWeight={600}>
                      {laudo.codigo_laudo}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {laudo.cliente.nome}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {laudo.cliente.codigo}
                    </Typography>
                  </TableCell>
                  <TableCell>{laudo.data_emissao}</TableCell>
                  <TableCell align="right" sx={{ whiteSpace: "nowrap" }}>
                    <Tooltip title="Ver detalhe">
                      <IconButton
                        size="small"
                        onClick={() => navigate(`/laudos/${laudo.id}`)}
                      >
                        <VisibilityIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>

                    <Tooltip title="Baixar PDF">
                      <IconButton
                        size="small"
                        color="primary"
                        onClick={() =>
                          void baixarPdf(laudo.id, laudo.codigo_laudo)
                        }
                      >
                        <PictureAsPdfIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>

                    {isStaff && (
                      <>
                        <Tooltip title="Editar">
                          <IconButton
                            size="small"
                            onClick={() =>
                              navigate(`/laudos/${laudo.id}/editar`)
                            }
                          >
                            <EditIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>

                        <Tooltip title="Excluir">
                          <IconButton
                            size="small"
                            color="error"
                            disabled={deletando === laudo.id}
                            onClick={() => setConfirmarExclusao(laudo.id)}
                          >
                            <DeleteIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <ConfirmDialog
        open={confirmarExclusao !== null}
        title="Excluir laudo"
        message={`Deseja excluir permanentemente o laudo ${laudoParaExcluir?.codigo_laudo ?? ""}? Esta ação não pode ser desfeita.`}
        confirmLabel="Excluir"
        loading={deletando !== null}
        onConfirm={async () => {
          if (confirmarExclusao !== null) {
            await excluir(confirmarExclusao);
            setConfirmarExclusao(null);
          }
        }}
        onCancel={() => setConfirmarExclusao(null)}
      />
    </Box>
  );
}
