import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CircularProgress,
  Typography,
} from "@mui/material";
import { NavLink } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { useLaudos } from "../../hooks/useLaudos";
import ClientDashboard from "./components/ClientDashboard";

const staffCards = [
  {
    title: "Laudos",
    description: "Criar e acompanhar laudos de análise.",
    to: "/laudos/novo",
  },
  {
    title: "Calibração",
    description: "Gerenciar baterias e curvas de calibração.",
    to: "/calibracao",
  },
  {
    title: "Operação em Lote",
    description: "Inserir leituras em lote na bancada.",
    to: "/entrada-lote",
  },
];

function StaffDashboard({ username }: { username: string }) {
  return (
    <Box>
      <Typography variant="h5" fontWeight={700} color="primary" gutterBottom>
        Olá, {username} 👋
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Acesso rápido às rotinas do laboratório.
      </Typography>
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "repeat(3, 1fr)" },
          gap: 2,
        }}
      >
        {staffCards.map((card) => (
          <Card key={card.to} variant="outlined">
            <CardContent>
              <Typography variant="h6" fontWeight={700} gutterBottom>
                {card.title}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {card.description}
              </Typography>
            </CardContent>
            <CardActions sx={{ px: 2, pb: 2 }}>
              <Button
                component={NavLink}
                to={card.to}
                variant="contained"
                size="small"
              >
                Acessar
              </Button>
            </CardActions>
          </Card>
        ))}
      </Box>
    </Box>
  );
}

function ClienteDashboardWrapper({ username }: { username: string }) {
  const { laudos, loading, baixarPdf } = useLaudos();

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} color="primary" gutterBottom>
        Olá, {username} 👋
      </Typography>
      <ClientDashboard laudos={laudos} onBaixarPdf={baixarPdf} />
    </Box>
  );
}

export default function DashboardPlaceholder() {
  const { user, isStaff } = useAuth();
  const username = user?.username ?? "";

  return isStaff ? (
    <StaffDashboard username={username} />
  ) : (
    <ClienteDashboardWrapper username={username} />
  );
}
