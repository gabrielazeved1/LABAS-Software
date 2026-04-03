/**
 * Placeholder temporário da Dashboard.
 * Substituir pela DashboardPage real na Sprint 2 da Sabrina.
 */
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { useAuth } from "../../hooks/useAuth";

export default function DashboardPlaceholder() {
  const { user } = useAuth();

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} color="primary" gutterBottom>
        Olá, {user?.username} 👋
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Dashboard em construção.
      </Typography>
    </Box>
  );
}
