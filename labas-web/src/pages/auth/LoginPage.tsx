/**
 * Página de Login do LABAS.
 *
 * Princípios SOLID (estrito):
 * - S: Apenas renderização/orquestração da UI.
 * - D: Recebe dependências (login) via hook, não acessa AuthContext diretamente.
 * - Validação e lógica de submit extraídas para arquivos próprios.
 */

import { useState } from "react";
import { Link as RouterLink, Navigate } from "react-router-dom";
import {
  Box,
  Button,
  CircularProgress,
  Alert,
  TextField,
  Typography,
  Link,
  InputAdornment,
  IconButton,
  Divider,
} from "@mui/material";
import {
  Visibility,
  VisibilityOff,
  ScienceOutlined,
  LoginOutlined,
} from "@mui/icons-material";
import { useAuth } from "../../hooks/useAuth";
import { useLoginForm } from "../../hooks/useLoginForm";

/**
 * Tela de login com formulário validado via `react-hook-form` + `zod`.
 * Rota pública: `/login`
 *
 * SOLID estrito: só renderiza/orquestra, lógica e validação externas.
 */
export default function LoginPage() {
  const { login, isAuthenticated, loading: authLoading } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    apiError,
    onSubmit,
  } = useLoginForm(login);
  const [showPassword, setShowPassword] = useState(false);

  if (!authLoading && isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      {/* Painel esquerdo — identidade visual (somente desktop) */}
      <Box
        sx={{
          display: { xs: "none", md: "flex" },
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          flex: 1,
          bgcolor: "primary.main",
          color: "primary.contrastText",
          p: 8,
          gap: 3,
        }}
      >
        <ScienceOutlined sx={{ fontSize: 80, opacity: 0.85 }} />
        <Box sx={{ textAlign: "center" }}>
          <Typography
            variant="h3"
            fontWeight={800}
            letterSpacing={1}
            gutterBottom
          >
            LABAS
          </Typography>
          <Typography variant="h6" fontWeight={400} sx={{ opacity: 0.85 }}>
            Laboratório de Análise de Solo
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.65, mt: 0.5 }}>
            Universidade Federal de Uberlândia
          </Typography>
        </Box>
        <Divider
          flexItem
          sx={{ borderColor: "rgba(255,255,255,0.2)", my: 1 }}
        />
        <Typography
          variant="body2"
          sx={{ opacity: 0.55, textAlign: "center", maxWidth: 300 }}
        >
          Gestão de análises laboratoriais e laudos técnicos para produtores
          rurais.
        </Typography>
      </Box>

      {/* Painel direito — formulário */}
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          width: { xs: "100%", md: 480 },
          px: { xs: 3, sm: 6 },
          py: 6,
          bgcolor: "background.paper",
        }}
      >
        {/* Marca compacta — apenas mobile */}
        <Box
          sx={{
            display: { xs: "block", md: "none" },
            textAlign: "center",
            mb: 5,
          }}
        >
          <Typography variant="h5" fontWeight={800} color="primary">
            LABAS
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Laboratório de Análise de Solo — UFU
          </Typography>
        </Box>

        <Typography variant="h5" fontWeight={700} gutterBottom>
          Bem-vindo de volta
        </Typography>
        <Typography variant="body2" color="text.secondary" mb={4}>
          Entre com suas credenciais para acessar o sistema.
        </Typography>

        {apiError && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {apiError}
          </Alert>
        )}

        <Box
          component="form"
          onSubmit={handleSubmit(onSubmit)}
          noValidate
          sx={{ display: "flex", flexDirection: "column", gap: 2.5 }}
        >
          <TextField
            label="Usuário"
            autoComplete="username"
            autoFocus
            fullWidth
            error={!!errors.username}
            helperText={errors.username?.message}
            {...register("username")}
          />

          <TextField
            label="Senha"
            type={showPassword ? "text" : "password"}
            autoComplete="current-password"
            fullWidth
            error={!!errors.password}
            helperText={errors.password?.message}
            slotProps={{
              input: {
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword((v) => !v)}
                      edge="end"
                      tabIndex={-1}
                      aria-label={
                        showPassword ? "Ocultar senha" : "Exibir senha"
                      }
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              },
            }}
            {...register("password")}
          />

          <Button
            type="submit"
            variant="contained"
            size="large"
            fullWidth
            disabled={isSubmitting}
            startIcon={!isSubmitting && <LoginOutlined />}
            sx={{ mt: 1, py: 1.5, fontWeight: 700, fontSize: "1rem" }}
          >
            {isSubmitting ? (
              <CircularProgress size={22} color="inherit" />
            ) : (
              "Entrar"
            )}
          </Button>
        </Box>

        <Divider sx={{ my: 4 }} />

        <Typography variant="body2" color="text.secondary" textAlign="center">
          Novo produtor rural?{" "}
          <Link
            component={RouterLink}
            to="/register"
            color="primary"
            fontWeight={600}
          >
            Criar conta
          </Link>
        </Typography>
      </Box>
    </Box>
  );
}
