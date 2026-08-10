import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Controller } from "react-hook-form";
import {
  Box,
  Button,
  CircularProgress,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useClienteForm } from "../../hooks/useClienteForm";
import { clienteService } from "../../services/clienteService";
import { useSnackbar } from "../../hooks/useSnackbar";
import type { Cliente } from "../../types/cliente";

function formatPhone(value: string): string {
  const d = value.replace(/\D/g, "").slice(0, 11);
  if (d.length <= 2) return d;
  if (d.length <= 6) return `(${d.slice(0, 2)}) ${d.slice(2)}`;
  if (d.length <= 10) return `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`;
  return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`;
}

export default function ClienteFormPage() {
  const { codigo } = useParams<{ codigo?: string }>();
  const navigate = useNavigate();
  const { showApiError } = useSnackbar();
  const edicao = !!codigo;

  const [clienteInicial, setClienteInicial] = useState<Cliente | undefined>();
  const [buscando, setBuscando] = useState(edicao);

  useEffect(() => {
    if (!edicao || !codigo) return;
    clienteService
      .buscar(codigo)
      .then(setClienteInicial)
      .catch(showApiError)
      .finally(() => setBuscando(false));
  }, [codigo, edicao, showApiError]);

  const { form, loading, onSubmit } = useClienteForm({
    clienteInicial,
    onSucesso: () => navigate("/clientes"),
  });

  const {
    control,
    formState: { errors },
  } = form;

  if (buscando) {
    return (
      <Box display="flex" justifyContent="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        pt: 2,
      }}
    >
      <Typography variant="h5" fontWeight={700} color="primary" gutterBottom>
        {edicao ? "Editar Cliente" : "Novo Cliente"}
      </Typography>

      <Paper variant="outlined" sx={{ p: 3, width: "100%", maxWidth: 560 }}>
        <Stack component="form" onSubmit={onSubmit} spacing={2}>
          <Controller
            name="codigo"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Código"
                placeholder="Ex: CLI-001"
                error={!!errors.codigo}
                helperText={errors.codigo?.message}
                disabled={edicao}
                required
              />
            )}
          />
          <Controller
            name="nome"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Nome / Razão Social"
                error={!!errors.nome}
                helperText={errors.nome?.message}
                required
              />
            )}
          />
          <Controller
            name="municipio"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Município"
                error={!!errors.municipio}
                helperText={errors.municipio?.message}
              />
            )}
          />
          <Controller
            name="area"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Área"
                error={!!errors.area}
                helperText={errors.area?.message}
              />
            )}
          />
          <Controller
            name="telefone"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                onChange={(e) => field.onChange(formatPhone(e.target.value))}
                label="Telefone"
                placeholder="(34) 99999-9999"
                inputProps={{ maxLength: 15 }}
                error={!!errors.telefone}
                helperText={errors.telefone?.message}
              />
            )}
          />
          <Controller
            name="email"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="E-mail"
                type="email"
                error={!!errors.email}
                helperText={errors.email?.message}
              />
            )}
          />
          <Controller
            name="observacoes"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Observações"
                multiline
                rows={3}
                error={!!errors.observacoes}
                helperText={errors.observacoes?.message}
              />
            )}
          />

          <Stack direction="row" spacing={1} justifyContent="flex-end">
            <Button variant="outlined" onClick={() => navigate("/clientes")}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained" disabled={loading}>
              {loading ? (
                <CircularProgress size={20} />
              ) : edicao ? (
                "Salvar"
              ) : (
                "Criar"
              )}
            </Button>
          </Stack>
        </Stack>
      </Paper>
    </Box>
  );
}
