import { useEffect, useMemo, useState } from "react";
import { Controller } from "react-hook-form";
import type { InputHTMLAttributes } from "react";
import {
  Alert,
  Autocomplete,
  Box,
  Button,
  CircularProgress,
  Grid,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { Link as RouterLink, useNavigate, useParams } from "react-router-dom";
import PageHeader from "../../components/shared/PageHeader";
import LoadingOverlay from "../../components/shared/LoadingOverlay";
import { useLaudoEditForm } from "../../hooks/useLaudoEditForm";
import { useClientes } from "../../hooks/useClientes";
import { laudoService } from "../../services/laudoService";
import { useSnackbar } from "../../hooks/useSnackbar";
import type { Cliente } from "../../types/cliente";
import type { AnaliseSolo } from "../../types/analise";
import type { LaudoForm } from "../../schemas/laudoSchemas";

const decimalInputProps = {
  inputMode: "decimal" as const,
  pattern: "[0-9]*[.,]?[0-9]*",
};

type FieldName = keyof LaudoForm;

type FieldConfig = {
  name: FieldName;
  label: string;
  inputProps?: InputHTMLAttributes<HTMLInputElement>;
};

const PH_FIELDS: FieldConfig[] = [
  { name: "ph_agua", label: "pH água" },
  { name: "ph_cacl2", label: "pH CaCl₂" },
  { name: "ph_kcl", label: "pH KCl" },
];

const ESPECTRO_FIELDS: FieldConfig[] = [
  { name: "p_m", label: "P Mehlich (mg/dm³)" },
  { name: "p_r", label: "P Resina (mg/dm³)" },
  { name: "p_rem", label: "P Rem (mg/L)" },
  { name: "mo", label: "Matéria Orgânica (dag/kg)" },
  { name: "s", label: "Enxofre (mg/dm³)" },
  { name: "b", label: "Boro (mg/dm³)" },
];

const FOTOMETRO_FIELDS: FieldConfig[] = [
  { name: "k", label: "Potássio (mg/dm³)" },
  { name: "na", label: "Sódio (mg/dm³)" },
];

const ABSORCAO_FIELDS: FieldConfig[] = [
  { name: "ca", label: "Cálcio (cmolc/dm³)" },
  { name: "mg", label: "Magnésio (cmolc/dm³)" },
  { name: "cu", label: "Cobre (mg/dm³)" },
  { name: "fe", label: "Ferro (mg/dm³)" },
  { name: "mn", label: "Manganês (mg/dm³)" },
  { name: "zn", label: "Zinco (mg/dm³)" },
];

const TITULACAO_FIELDS: FieldConfig[] = [
  { name: "al", label: "Alumínio (cmolc/dm³)" },
  { name: "h_al", label: "Acidez Potencial (cmolc/dm³)" },
];

const GRANULOMETRIA_FIELDS: FieldConfig[] = [
  { name: "areia", label: "Areia (%)" },
  { name: "argila", label: "Argila (%)" },
  { name: "silte", label: "Silte (%)" },
];

const renderNumberField = (
  field: FieldConfig,
  getErrorMessage: (name: FieldName) => string | undefined,
  register: ReturnType<typeof useLaudoEditForm>["form"]["register"],
  disabled: boolean,
) => (
  <Grid size={{ xs: 12, sm: 6, md: 4 }} key={field.name}>
    <TextField
      fullWidth
      size="small"
      label={field.label}
      type="text"
      inputProps={field.inputProps ?? decimalInputProps}
      error={!!getErrorMessage(field.name)}
      helperText={getErrorMessage(field.name)}
      disabled={disabled}
      {...register(field.name)}
    />
  </Grid>
);

export default function LaudoEditPage() {
  const { nLab: nLabParam } = useParams<{ nLab: string }>();
  const navigate = useNavigate();
  const { showApiError } = useSnackbar();

  const [laudo, setLaudo] = useState<AnaliseSolo | undefined>();
  const [buscando, setBuscando] = useState(true);
  const [erroFetch, setErroFetch] = useState(false);

  const [clienteSelecionado, setClienteSelecionado] = useState<Cliente | null>(
    null,
  );
  const [clienteInput, setClienteInput] = useState("");

  const { clientes, loading: clientesLoading, buscar, limpar } = useClientes();
  const { form, submitting, onSubmit } = useLaudoEditForm(laudo);

  useEffect(() => {
    if (!nLabParam) {
      navigate("/laudos");
      return;
    }
    laudoService
      .buscar(decodeURIComponent(nLabParam))
      .then((data) => {
        setLaudo(data);
        setClienteSelecionado(data.cliente);
        setClienteInput(`${data.cliente.codigo} — ${data.cliente.nome}`);
      })
      .catch((err) => {
        showApiError(err);
        setErroFetch(true);
      })
      .finally(() => setBuscando(false));
  }, [nLabParam, navigate, showApiError]);

  // Garante que o cliente atual sempre aparece na lista de opções do Autocomplete
  const clientesOpcoes = useMemo(() => {
    if (!clienteSelecionado) return clientes;
    if (clientes.some((c) => c.codigo === clienteSelecionado.codigo))
      return clientes;
    return [clienteSelecionado, ...clientes];
  }, [clientes, clienteSelecionado]);

  const getErrorMessage = (name: FieldName) =>
    form.formState.errors[name]?.message as string | undefined;

  const handleClienteInput = (_: React.SyntheticEvent, value: string) => {
    setClienteInput(value);
    if (value.trim().length === 0) {
      if (clienteSelecionado) {
        setClienteSelecionado(null);
        form.setValue("cliente_codigo", "", {
          shouldDirty: true,
          shouldValidate: true,
        });
      }
      limpar();
      return;
    }
    if (value.trim().length < 2) {
      limpar();
      return;
    }
    buscar(value);
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
          Não foi possível carregar o laudo. Verifique o número e tente
          novamente.
        </Alert>
        <Button variant="outlined" component={RouterLink} to="/laudos">
          Voltar para laudos
        </Button>
      </Box>
    );
  }

  return (
    <Box component="form" onSubmit={onSubmit} noValidate>
      <LoadingOverlay open={submitting} message="Salvando alterações..." />

      <PageHeader
        title={`Editar Laudo ${laudo.n_lab}`}
        subtitle="Atualize os dados da análise de solo"
      />

      {/* ── Dados gerais ─────────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Dados gerais
        </Typography>
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <TextField
              fullWidth
              size="small"
              label="Nº do laudo"
              value={laudo.n_lab}
              disabled
              InputProps={{ readOnly: true }}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <TextField
              fullWidth
              size="small"
              label="Data de entrada"
              type="date"
              InputLabelProps={{ shrink: true }}
              error={!!getErrorMessage("data_entrada")}
              helperText={getErrorMessage("data_entrada")}
              disabled={submitting}
              {...form.register("data_entrada")}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <TextField
              fullWidth
              size="small"
              label="Data de saída"
              type="date"
              InputLabelProps={{ shrink: true }}
              error={!!getErrorMessage("data_saida")}
              helperText={getErrorMessage("data_saida")}
              disabled={submitting}
              {...form.register("data_saida")}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 8 }}>
            <Controller
              control={form.control}
              name="cliente_codigo"
              render={({ field, fieldState }) => (
                <Autocomplete
                  options={clientesOpcoes}
                  value={clienteSelecionado}
                  inputValue={clienteInput}
                  onInputChange={handleClienteInput}
                  onChange={(_, value) => {
                    setClienteSelecionado(value);
                    field.onChange(value?.codigo ?? "");
                  }}
                  onBlur={field.onBlur}
                  loading={clientesLoading}
                  noOptionsText={
                    clienteInput.length < 2
                      ? "Digite pelo menos 2 caracteres"
                      : "Nenhum cliente encontrado"
                  }
                  getOptionLabel={(option) =>
                    `${option.codigo} — ${option.nome}`
                  }
                  isOptionEqualToValue={(option, value) =>
                    option.codigo === value.codigo
                  }
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Cliente"
                      size="small"
                      error={!!fieldState.error}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />
              )}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              size="small"
              label="Código do cliente"
              value={clienteSelecionado?.codigo ?? ""}
              InputProps={{ readOnly: true }}
              placeholder="Selecione um cliente"
            />
          </Grid>

          {clienteSelecionado && (
            <Grid size={12}>
              <Typography variant="body2" color="text.secondary">
                {clienteSelecionado.municipio} • {clienteSelecionado.area}
              </Typography>
            </Grid>
          )}
        </Grid>
      </Paper>

      {/* ── pH-metro ──────────────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          pH-metro
        </Typography>
        <Grid container spacing={2}>
          {PH_FIELDS.map((field) =>
            renderNumberField(
              field,
              getErrorMessage,
              form.register,
              submitting,
            ),
          )}
        </Grid>
      </Paper>

      {/* ── Espectrofotômetro ─────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Espectrofotômetro
        </Typography>
        <Grid container spacing={2}>
          {ESPECTRO_FIELDS.map((field) =>
            renderNumberField(
              field,
              getErrorMessage,
              form.register,
              submitting,
            ),
          )}
        </Grid>
      </Paper>

      {/* ── Fotômetro de chama ────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Fotômetro de chama
        </Typography>
        <Grid container spacing={2}>
          {FOTOMETRO_FIELDS.map((field) =>
            renderNumberField(
              field,
              getErrorMessage,
              form.register,
              submitting,
            ),
          )}
        </Grid>
      </Paper>

      {/* ── Absorção atômica ──────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Absorção atômica
        </Typography>
        <Grid container spacing={2}>
          {ABSORCAO_FIELDS.map((field) =>
            renderNumberField(
              field,
              getErrorMessage,
              form.register,
              submitting,
            ),
          )}
        </Grid>
      </Paper>

      {/* ── Titulação ─────────────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Titulação
        </Typography>
        <Grid container spacing={2}>
          {TITULACAO_FIELDS.map((field) =>
            renderNumberField(
              field,
              getErrorMessage,
              form.register,
              submitting,
            ),
          )}
        </Grid>
      </Paper>

      {/* ── Granulometria ─────────────────────────────────────────────────── */}
      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Granulometria
        </Typography>
        <Grid container spacing={2}>
          {GRANULOMETRIA_FIELDS.map((field) =>
            renderNumberField(
              field,
              getErrorMessage,
              form.register,
              submitting,
            ),
          )}
        </Grid>
      </Paper>

      <Stack direction={{ xs: "column", sm: "row" }} spacing={2} mb={4}>
        <Button variant="outlined" component={RouterLink} to="/laudos">
          Voltar
        </Button>
        <Button type="submit" variant="contained" disabled={submitting}>
          {submitting ? "Salvando..." : "Salvar alterações"}
        </Button>
      </Stack>
    </Box>
  );
}
