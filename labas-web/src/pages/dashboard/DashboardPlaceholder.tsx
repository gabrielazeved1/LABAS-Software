import { Box, CircularProgress, Typography } from "@mui/material";
import { useAuth } from "../../hooks/useAuth";
import { useLaudos } from "../../hooks/useLaudos";
import ClientDashboard from "./components/ClientDashboard";
import StaffDashboard from "./StaffDashboard";

function ClienteDashboardWrapper() {
  const { laudos, loading, baixarPdf } = useLaudos();

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  return <ClientDashboard laudos={laudos} onBaixarPdf={baixarPdf} />;
}

export default function DashboardPlaceholder() {
  const { isStaff, user } = useAuth();
  const username = user?.username ?? "";

  return isStaff ? (
    <StaffDashboard username={username} />
  ) : (
    <ClienteDashboardWrapper />
  );
}
