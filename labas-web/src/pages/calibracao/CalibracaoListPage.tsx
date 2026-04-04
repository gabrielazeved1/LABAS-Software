import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Chip,
  CircularProgress,
  IconButton,
  Switch,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Tabs,
  Tooltip,
  Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import TuneIcon from "@mui/icons-material/Tune";
import { useCalibracao } from "../../hooks/useCalibracao";
import ConfirmDialog from "../../components/shared/ConfirmDialog";
import EmptyState from "../../components/shared/EmptyState";
import PageHeader from "../../components/shared/PageHeader";
import { SEM_CURVA_CALIBRACAO } from "../../config/calibracaoConstants";
import type { Equipamento } from "../../types/calibracao";

const EQUIPAMENTOS: { value: Equipamento; label: string }[] = [
  { value: "AA", label: "Absorção Atômica" },
  { value: "FC", label: "Fotômetro de Chama" },
  { value: "ES", label: "Espectrofotômetro" },
  { value: "TI", label: "Titulação" },
  { value: "PH", label: "pH-metro" },
];

export default function CalibracaoListPage() {
  const navigate = useNavigate();
  const [tabIndex, setTabIndex] = useState(0);
  const [confirmarRemocaoId, setConfirmarRemocaoId] = useState<number | null>(
    null,
  );

  const equipamentoAtivo = EQUIPAMENTOS[tabIndex].value;
  const {
    baterias,
    loading,
    setEquipamentoFiltro,
    toggleAtivo,
    removerBateria,
  } = useCalibracao();

  const handleTabChange = (_: React.SyntheticEvent, newIndex: number) => {
    setTabIndex(newIndex);
    setEquipamentoFiltro(EQUIPAMENTOS[newIndex].value);
  };

  const handleConfirmarRemocao = async () => {
    if (confirmarRemocaoId !== null) {
      await removerBateria(confirmarRemocaoId);
      setConfirmarRemocaoId(null);
    }
  };

  const bateriasFiltradas = baterias.filter(
    (b) => b.equipamento === equipamentoAtivo,
  );

  return (
    <Box>
      <PageHeader
        title="Calibração de Equipamentos"
        actions={
          <IconButton
            color="primary"
            onClick={() =>
              navigate("/calibracao/nova", {
                state: { equipamento: equipamentoAtivo },
              })
            }
            aria-label="Nova Bateria"
          >
            <AddIcon />
          </IconButton>
        }
      />

      <Tabs
        value={tabIndex}
        onChange={handleTabChange}
        sx={{ mb: 3, borderBottom: 1, borderColor: "divider" }}
        aria-label="Abas de equipamentos"
      >
        {EQUIPAMENTOS.map((eq) => (
          <Tab key={eq.value} label={eq.label} />
        ))}
      </Tabs>

      {loading ? (
        <Box display="flex" justifyContent="center" py={6}>
          <CircularProgress />
        </Box>
      ) : bateriasFiltradas.length === 0 ? (
        <EmptyState
          title="Nenhuma bateria encontrada"
          description={`Nenhuma bateria de ${EQUIPAMENTOS[tabIndex].label} cadastrada ainda.`}
          action={
            <Button
              variant="outlined"
              size="small"
              onClick={() =>
                navigate("/calibracao/nova", {
                  state: { equipamento: equipamentoAtivo },
                })
              }
            >
              Nova Bateria
            </Button>
          }
        />
      ) : (
        <Table size="small" aria-label="Baterias de calibração">
          <TableHead>
            <TableRow>
              <TableCell>Elemento</TableCell>
              <TableCell>Data</TableCell>
              <TableCell>Equação</TableCell>
              <TableCell align="center">R²</TableCell>
              <TableCell align="center">Ativa</TableCell>
              <TableCell align="center">Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {bateriasFiltradas.map((bateria) => (
              <TableRow key={bateria.id} hover>
                <TableCell>{bateria.elemento}</TableCell>
                <TableCell>
                  {new Date(bateria.data_criacao).toLocaleDateString("pt-BR")}
                </TableCell>
                <TableCell>
                  {SEM_CURVA_CALIBRACAO.includes(bateria.equipamento) ? (
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      fontStyle="italic"
                    >
                      Não utiliza equação
                    </Typography>
                  ) : (
                    <Typography variant="body2" fontFamily="monospace">
                      {bateria.equacao_formada}
                    </Typography>
                  )}
                </TableCell>
                <TableCell align="center">
                  {SEM_CURVA_CALIBRACAO.includes(bateria.equipamento) ? (
                    <Typography variant="body2" color="text.secondary">
                      —
                    </Typography>
                  ) : bateria.r_quadrado !== null ? (
                    <Chip
                      size="small"
                      label={Number(bateria.r_quadrado).toFixed(4)}
                      color={
                        Number(bateria.r_quadrado) >= 0.99
                          ? "success"
                          : "warning"
                      }
                    />
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      —
                    </Typography>
                  )}
                </TableCell>
                <TableCell align="center">
                  <Switch
                    checked={bateria.ativo}
                    onChange={(e) => toggleAtivo(bateria.id, e.target.checked)}
                    color="success"
                    slotProps={{
                      input: { "aria-label": `Ativar bateria ${bateria.id}` },
                    }}
                  />
                </TableCell>
                <TableCell align="center">
                  <Tooltip title="Ver / Editar pontos">
                    <IconButton
                      size="small"
                      onClick={() => navigate(`/calibracao/${bateria.id}`)}
                      aria-label={`Editar bateria ${bateria.id}`}
                    >
                      <TuneIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Remover bateria">
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => setConfirmarRemocaoId(bateria.id)}
                      aria-label={`Remover bateria ${bateria.id}`}
                    >
                      <DeleteOutlineIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      <ConfirmDialog
        open={confirmarRemocaoId !== null}
        title="Remover bateria"
        message="Esta ação removerá a bateria e todos os seus pontos de calibração. Deseja continuar?"
        onConfirm={handleConfirmarRemocao}
        onCancel={() => setConfirmarRemocaoId(null)}
      />
    </Box>
  );
}
