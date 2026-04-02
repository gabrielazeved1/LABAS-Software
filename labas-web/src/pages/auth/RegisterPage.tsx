/**
 * Página de cadastro de novo cliente (Produtor Rural) do LABAS.
 *
 * Princípios SOLID (estrito):
 * - S: Apenas renderização/orquestração dos steps.
 * - D: Recebe dependências (register, login, navigate) via hook customizado.
 * - Validação e lógica de submit extraídas para arquivos próprios.
 */

import { Link as RouterLink, useNavigate } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Link,
  Paper,
  Step,
  StepLabel,
  Stepper,
  TextField,
  Typography,
} from "@mui/material";
import { authService } from "../../services/authService";
import { useAuth } from "../../hooks/useAuth";
import { useRegisterForm } from "../../hooks/useRegisterForm";

// Schemas e tipos importados de src/validators/registerSchema.ts

// ---------------------------------------------------------------------------
// Constantes
// ---------------------------------------------------------------------------

const STEPS = ["Credenciais", "Dados do cliente"];

// ---------------------------------------------------------------------------
// Componente
// ---------------------------------------------------------------------------

/**
 * Tela de cadastro de novos clientes.
 * Rota pública: `/register`
 *
 * SOLID estrito: só renderiza/orquestra, lógica e validação externas.
 */
export default function RegisterPage() {
  const navigate = useNavigate();
  const { register: registerApi } = authService;
  const { login } = useAuth();
  // Wrapper para SOLID-D: abstrai retorno do register para Promise<void>
  const registerFn = async (payload: any) => {
    await registerApi(payload);
  };
  const {
    activeStep,
    setActiveStep,
    apiError,
    form1,
    form2,
    handleStep1Submit,
    handleStep2Submit,
  } = useRegisterForm(registerFn, login, navigate);

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        bgcolor: "background.default",
        px: 2,
      }}
    >
      <Paper
        elevation={3}
        sx={{
          width: "100%",
          maxWidth: 480,
          p: { xs: 3, sm: 4 },
          borderRadius: 2,
        }}
      >
        {/* Cabeçalho */}
        <Box sx={{ textAlign: "center", mb: 3 }}>
          <Typography variant="h5" fontWeight={700} color="primary">
            LABAS
          </Typography>
          <Typography variant="body2" color="text.secondary" mt={0.5}>
            Laboratório de Análise de Solo — UFU
          </Typography>
        </Box>

        <Typography variant="h6" fontWeight={600} mb={3}>
          Criar conta
        </Typography>

        {/* Stepper */}
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {STEPS.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {/* Erro da API */}
        {apiError && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {apiError}
          </Alert>
        )}

        {/* ---- Step 1: Credenciais ---- */}
        {activeStep === 0 && (
          <Box
            component="form"
            onSubmit={form1.handleSubmit(handleStep1Submit)}
            noValidate
            sx={{ display: "flex", flexDirection: "column", gap: 2 }}
          >
            <TextField
              label="Usuário"
              autoFocus
              fullWidth
              error={!!form1.formState.errors.username}
              helperText={form1.formState.errors.username?.message}
              {...form1.register("username")}
            />
            <TextField
              label="E-mail"
              type="email"
              fullWidth
              error={!!form1.formState.errors.email}
              helperText={form1.formState.errors.email?.message}
              {...form1.register("email")}
            />
            <TextField
              label="Senha"
              type="password"
              fullWidth
              error={!!form1.formState.errors.password}
              helperText={form1.formState.errors.password?.message}
              {...form1.register("password")}
            />
            <TextField
              label="Confirmar senha"
              type="password"
              fullWidth
              error={!!form1.formState.errors.password2}
              helperText={form1.formState.errors.password2?.message}
              {...form1.register("password2")}
            />
            <Button
              type="submit"
              variant="contained"
              size="large"
              fullWidth
              sx={{ mt: 1 }}
            >
              Próximo
            </Button>
          </Box>
        )}

        {/* ---- Step 2: Dados do cliente ---- */}
        {activeStep === 1 && (
          <Box
            component="form"
            onSubmit={form2.handleSubmit(handleStep2Submit)}
            noValidate
            sx={{ display: "flex", flexDirection: "column", gap: 2 }}
          >
            <TextField
              label="Nome completo"
              autoFocus
              fullWidth
              error={!!form2.formState.errors.nome_cliente}
              helperText={form2.formState.errors.nome_cliente?.message}
              {...form2.register("nome_cliente")}
            />
            <TextField
              label="Código do cliente"
              fullWidth
              error={!!form2.formState.errors.codigo_cliente}
              helperText={form2.formState.errors.codigo_cliente?.message}
              {...form2.register("codigo_cliente")}
            />
            <TextField
              label="Município"
              fullWidth
              error={!!form2.formState.errors.municipio}
              helperText={form2.formState.errors.municipio?.message}
              {...form2.register("municipio")}
            />
            <TextField
              label="Área (ha)"
              type="number"
              fullWidth
              inputProps={{ step: "0.01", min: 0 }}
              error={!!form2.formState.errors.area}
              helperText={form2.formState.errors.area?.message}
              {...form2.register("area")}
            />

            <Box sx={{ display: "flex", gap: 1, mt: 1 }}>
              <Button
                variant="outlined"
                size="large"
                fullWidth
                onClick={() => setActiveStep(0)}
                disabled={form2.formState.isSubmitting}
              >
                Voltar
              </Button>
              <Button
                type="submit"
                variant="contained"
                size="large"
                fullWidth
                disabled={form2.formState.isSubmitting}
              >
                {form2.formState.isSubmitting ? (
                  <CircularProgress size={24} color="inherit" />
                ) : (
                  "Criar conta"
                )}
              </Button>
            </Box>
          </Box>
        )}

        {/* Link para login */}
        <Box sx={{ textAlign: "center", mt: 3 }}>
          <Typography variant="body2" color="text.secondary">
            Já tem conta?{" "}
            <Link component={RouterLink} to="/login" color="primary">
              Entrar
            </Link>
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
}
