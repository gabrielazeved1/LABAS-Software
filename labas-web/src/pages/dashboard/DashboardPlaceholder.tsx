/**
 * Placeholder temporário da Dashboard.
 * Substituir pela Dashboard real no Sprint 1.
 * @module DashboardPlaceholder
 */
import { Box, Button, Typography } from "@mui/material";
import { LogoutOutlined } from "@mui/icons-material";
import { useAuth } from "../../hooks/useAuth";

export default function DashboardPlaceholder() {
  const { user, logout } = useAuth();

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 2,
        bgcolor: "background.default",
      }}
    >
      <Typography variant="h5" fontWeight={700} color="primary">
        Olá, {user?.username} 👋
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Dashboard em construção.
      </Typography>
      <Button
        variant="outlined"
        color="error"
        startIcon={<LogoutOutlined />}
        onClick={logout}
      >
        Sair
      </Button>
    </Box>
  );
}
