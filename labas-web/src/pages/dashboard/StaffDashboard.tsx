import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Skeleton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Paper,
} from "@mui/material";
import AssignmentIcon from "@mui/icons-material/Assignment";
import ScienceIcon from "@mui/icons-material/Science";
import PeopleIcon from "@mui/icons-material/People";
import BatteryChargingFullIcon from "@mui/icons-material/BatteryChargingFull";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import BiotechIcon from "@mui/icons-material/Biotech";
import { useNavigate } from "react-router-dom";
import { NavLink } from "react-router-dom";
import { useDashboardStats } from "../../hooks/useDashboardStats";
import { useDashboardLaudos } from "../../hooks/useDashboardLaudos";

interface KpiCardProps {
  label: string;
  value: number | undefined;
  loading: boolean;
  icon: React.ReactNode;
}

function KpiCard({ label, value, loading, icon }: KpiCardProps) {
  return (
    <Card
      elevation={0}
      sx={{
        bgcolor: "primary.main",
        color: "white",
        border: "none",
      }}
    >
      <CardContent sx={{ display: "flex", alignItems: "center", gap: 2 }}>
        <Box
          sx={{
            bgcolor: "rgba(255,255,255,0.15)",
            borderRadius: 2,
            p: 1.5,
            display: "flex",
            alignItems: "center",
            color: "white",
          }}
        >
          {icon}
        </Box>
        <Box>
          <Typography
            variant="caption"
            sx={{ color: "rgba(255,255,255,0.75)", display: "block" }}
          >
            {label}
          </Typography>
          {loading ? (
            <Skeleton
              width={48}
              height={32}
              sx={{ bgcolor: "rgba(255,255,255,0.2)" }}
            />
          ) : (
            <Typography variant="h5" fontWeight={700} sx={{ color: "white" }}>
              {value ?? 0}
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
}

const acoesRapidas = [
  { label: "Novo Laudo", to: "/laudos/novo", variant: "contained" as const },
  {
    label: "Nova Calibração",
    to: "/calibracao/nova",
    variant: "outlined" as const,
  },
  {
    label: "Entrada de Amostras",
    to: "/entrada-lote",
    variant: "outlined" as const,
  },
];

export default function StaffDashboard({
  username: _username,
}: {
  username: string;
}) {
  const navigate = useNavigate();
  const { stats, loading: loadingStats } = useDashboardStats();
  const { laudos, loading: loadingLaudos } = useDashboardLaudos();

  const hoje = new Date().toLocaleDateString("pt-BR", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  const kpis = [
    {
      label: "Laudos Totais",
      value: stats?.total_laudos,
      icon: <AssignmentIcon />,
    },
    {
      label: "Laudos este Mês",
      value: stats?.laudos_mes,
      icon: <CalendarMonthIcon />,
    },
    {
      label: "Amostras Totais",
      value: stats?.total_amostras,
      icon: <BiotechIcon />,
    },
    {
      label: "Amostras este Mês",
      value: stats?.amostras_mes,
      icon: <ScienceIcon />,
    },
    {
      label: "Clientes Cadastrados",
      value: stats?.total_clientes,
      icon: <PeopleIcon />,
    },
    {
      label: "Baterias Ativas",
      value: stats?.baterias_ativas,
      icon: <BatteryChargingFullIcon />,
    },
  ];

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} color="primary" gutterBottom>
        Painel do Laboratório
      </Typography>
      <Typography
        variant="body2"
        color="text.secondary"
        sx={{ mb: 3, textTransform: "capitalize" }}
      >
        {hoje}
      </Typography>

      {/* KPIs */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        {kpis.map((kpi) => (
          <Grid size={{ xs: 12, sm: 6, md: 4 }} key={kpi.label}>
            <KpiCard
              label={kpi.label}
              value={kpi.value}
              loading={loadingStats}
              icon={kpi.icon}
            />
          </Grid>
        ))}
      </Grid>

      {/* Laudos recentes + Ações rápidas */}
      <Grid container spacing={3}>
        {/* Tabela de laudos recentes */}
        <Grid size={{ xs: 12, md: 8 }}>
          <Typography variant="h6" fontWeight={600} gutterBottom>
            Laudos Recentes
          </Typography>
          <TableContainer component={Paper} variant="outlined">
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Código</TableCell>
                  <TableCell>Cliente</TableCell>
                  <TableCell>Data Entrada</TableCell>
                  <TableCell align="right">Amostras</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loadingLaudos
                  ? Array.from({ length: 5 }).map((_, i) => (
                      <TableRow key={i}>
                        <TableCell>
                          <Skeleton />
                        </TableCell>
                        <TableCell>
                          <Skeleton />
                        </TableCell>
                        <TableCell>
                          <Skeleton />
                        </TableCell>
                        <TableCell>
                          <Skeleton />
                        </TableCell>
                      </TableRow>
                    ))
                  : laudos.map((l) => (
                      <TableRow
                        key={l.id}
                        hover
                        onClick={() => navigate(`/laudos/${l.id}`)}
                        sx={{ cursor: "pointer" }}
                      >
                        <TableCell>{l.codigo_laudo}</TableCell>
                        <TableCell>{l.cliente_nome}</TableCell>
                        <TableCell>
                          {new Date(l.data_emissao).toLocaleDateString("pt-BR")}
                        </TableCell>
                        <TableCell align="right">{l.total_analises}</TableCell>
                      </TableRow>
                    ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>

        {/* Ações rápidas */}
        <Grid size={{ xs: 12, md: 4 }}>
          <Typography variant="h6" fontWeight={600} gutterBottom>
            Ações Rápidas
          </Typography>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 1.5 }}>
            {acoesRapidas.map((acao) => (
              <Button
                key={acao.to}
                component={NavLink}
                to={acao.to}
                variant={acao.variant}
                fullWidth
              >
                {acao.label}
              </Button>
            ))}
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
}
