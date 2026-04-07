import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  Grid,
  Paper,
  Stack,
  Tooltip,
  Typography,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import EditIcon from "@mui/icons-material/Edit";
import { Link as RouterLink, useParams } from "react-router-dom";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import PageHeader from "../../components/shared/PageHeader";
import LoadingOverlay from "../../components/shared/LoadingOverlay";
import { laudoService } from "../../services/laudoService";
import { useAnalises } from "../../hooks/useAnalises";
import { useSnackbar } from "../../hooks/useSnackbar";
import { useAuth } from "../../hooks/useAuth";
import type { Laudo, AnaliseSolo } from "../../types/analise";

// ─── Colunas do DataGrid (somente leitura) ───────────────────────────────────

const colunas: GridColDef<AnaliseSolo>[] = [
  { field: "n_lab", headerName: "N° Lab", width: 110 },
  {
    field: "referencia",
    headerName: "Referência",
    width: 150,
    valueGetter: (_val, row) => row.referencia ?? "—",
  },
  { field: "data_entrada", headerName: "Data Entrada", width: 120 },
  {
    field: "ativo",
    headerName: "Status",
    width: 100,
    renderCell: ({ value }) =>
      value ? (
        <Chip label="Ativa" color="success" size="small" />
      ) : (
        <Chip label="Inativa" size="small" />
      ),
  },
  {
    field: "sb",
    headerName: "SB",
    width: 90,
    type: "number",
    valueGetter: (_val, row) => row.sb ?? "—",
  },
  {
    field: "T_maiusculo",
    headerName: "CTC",
    width: 90,
    type: "number",
    valueGetter: (_val, row) => row.T_maiusculo ?? "—",
  },
  {
    field: "V",
    headerName: "V%",
    width: 80,
    type: "number",
    valueGetter: (_val, row) => row.V ?? "—",
  },
  {
    field: "m",
    headerName: "m%",
    width: 80,
    type: "number",
    valueGetter: (_val, row) => row.m ?? "—",
  },
  {
    field: "ph_agua",
    headerName: "pH (água)",
    width: 100,
    type: "number",
    valueGetter: (_val, row) => row.ph_agua ?? "—",
  },
];

// ─── Componente ──────────────────────────────────────────────────────────────

export default function LaudoDetalhePage() {
  const { id: idParam } = useParams<{ id: string }>();
  const laudoId = idParam ? parseInt(idParam, 10) : undefined;

  const { isStaff } = useAuth();
  const { showApiError } = useSnackbar();

  const [laudo, setLaudo] = useState<Laudo | null>(null);
  const [buscando, setBuscando] = useState(true);
  const [erroFetch, setErroFetch] = useState(false);
  const [baixando, setBaixando] = useState(false);

  const { analises, loading: analisesLoading } = useAnalises(laudoId);

  useEffect(() => {
    if (!laudoId || isNaN(laudoId)) {
      setErroFetch(true);
      setBuscando(false);
      return;
    }
    laudoService
      .buscar(laudoId)
      .then(setLaudo)
      .catch((err) => {
        showApiError(err);
        setErroFetch(true);
      })
      .finally(() => setBuscando(false));
  }, [laudoId, showApiError]);

  const handleBaixarPdf = async () => {
    if (!laudo) return;
    setBaixando(true);
    try {
      const blob = await laudoService.baixarPdf(laudo.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `laudo-${laudo.codigo_laudo}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      showApiError(err);
    } finally {
      setBaixando(false);
    }
  };

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
          Não foi possível carregar o laudo. Verifique o identificador e tente
          novamente.
        </Alert>
        <Button variant="outlined" component={RouterLink} to="/laudos">
          Voltar para laudos
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <LoadingOverlay open={baixando} message="Gerando PDF..." />

      <PageHeader
        title={`Laudo ${laudo.codigo_laudo}`}
        subtitle={`${laudo.cliente.nome} (${laudo.cliente.codigo})`}
      />

      {/* ── Cabeçalho ──────────────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Dados do laudo
        </Typography>
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Typography variant="caption" color="text.secondary">
              Código
            </Typography>
            <Typography variant="body1" fontWeight={600}>
              {laudo.codigo_laudo}
            </Typography>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Typography variant="caption" color="text.secondary">
              Data de Emissão
            </Typography>
            <Typography variant="body1">{laudo.data_emissao}</Typography>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Typography variant="caption" color="text.secondary">
              Cliente
            </Typography>
            <Typography variant="body1">{laudo.cliente.nome}</Typography>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Typography variant="caption" color="text.secondary">
              Município
            </Typography>
            <Typography variant="body1">
              {laudo.cliente.municipio ?? "—"}
            </Typography>
          </Grid>

          {laudo.observacoes && (
            <Grid size={12}>
              <Divider sx={{ my: 1 }} />
              <Typography variant="caption" color="text.secondary">
                Observações
              </Typography>
              <Typography variant="body2" sx={{ whiteSpace: "pre-line" }}>
                {laudo.observacoes}
              </Typography>
            </Grid>
          )}
        </Grid>
      </Paper>

      {/* ── Análises ───────────────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Análises ({analises.filter((a) => a.ativo).length} ativas)
        </Typography>
        <Box sx={{ height: 400 }}>
          <DataGrid
            rows={analises}
            columns={colunas}
            loading={analisesLoading}
            density="compact"
            disableRowSelectionOnClick
            pageSizeOptions={[10, 25, 50]}
            initialState={{ pagination: { paginationModel: { pageSize: 10 } } }}
          />
        </Box>
      </Paper>

      {/* ── Ações ──────────────────────────────────────────────────────────── */}
      <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
        <Button variant="outlined" component={RouterLink} to="/laudos">
          Voltar
        </Button>

        <Tooltip title="Baixar PDF com todas as análises ativas">
          <span>
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={() => void handleBaixarPdf()}
              disabled={baixando}
            >
              {baixando ? "Gerando..." : "Gerar PDF"}
            </Button>
          </span>
        </Tooltip>

        {isStaff && (
          <Button
            variant="outlined"
            startIcon={<EditIcon />}
            component={RouterLink}
            to={`/laudos/${laudo.id}/editar`}
          >
            Editar
          </Button>
        )}
      </Stack>
    </Box>
  );
}
