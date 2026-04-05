import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import {
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  FormControlLabel,
  IconButton,
  MenuItem,
  Paper,
  Stack,
  Step,
  StepLabel,
  Stepper,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import PageHeader from "../../components/shared/PageHeader";
import { useBateriaDetalhe } from "../../hooks/useBateriaDetalhe";
import { useCalibracaoForm } from "../../hooks/useCalibracaoForm";
import {
  EQUIPAMENTOS,
  CALIBRACAO_STEPS,
  REQUER_VOLUMES,
  REQUER_BRANCO,
  LEITURA_LABEL,
  SEM_CURVA_CALIBRACAO,
  ELEMENTOS_POR_EQUIPAMENTO,
  ELEMENTO_LABEL,
} from "../../config/calibracaoConstants";
import type { Equipamento } from "../../types/calibracao";

export default function CalibracaoFormPage() {
  const { id } = useParams<{ id?: string }>();
  const location = useLocation();
  const bateriaId = id ? Number(id) : null;
  const isEdicao = bateriaId !== null;
  const equipamentoInicial = (
    location.state as { equipamento?: Equipamento } | null
  )?.equipamento;

  const {
    bateria,
    loading: loadingBateria,
    removerPonto,
    atualizarBateria,
    salvandoParametros,
  } = useBateriaDetalhe(bateriaId);
  const {
    bateriaForm,
    linhas,
    salvandoPontos,
    activeStep,
    submittingBateria,
    setActiveStep,
    handleCriarBateria,
    handleAdicionarLinhas,
    handleAtualizarLinha,
    handleRemoverLinha,
    handleFinalizar,
  } = useCalibracaoForm(bateriaId ?? undefined, equipamentoInicial);

  const equipamento = bateria?.equipamento ?? bateriaForm.watch("equipamento");
  const leituraLabel = LEITURA_LABEL[equipamento];
  const elementosFiltrados = ELEMENTOS_POR_EQUIPAMENTO[equipamento];

  const [parametros, setParametros] = useState({
    volume_solo: "",
    volume_extrator: "",
    leitura_branco: "",
  });

  const normalizeDecimalInput = (value: string) =>
    value.replace(/,/g, ".").trim();

  const normalizeDecimalOptional = (value: string) => {
    const normalized = normalizeDecimalInput(value);
    return normalized === "" ? undefined : normalized;
  };

  useEffect(() => {
    if (!bateria) return;
    setParametros({
      volume_solo:
        bateria.volume_solo !== null ? String(bateria.volume_solo) : "",
      volume_extrator:
        bateria.volume_extrator !== null ? String(bateria.volume_extrator) : "",
      leitura_branco:
        bateria.leitura_branco !== null ? String(bateria.leitura_branco) : "",
    });
  }, [bateria]);

  useEffect(() => {
    if (!isEdicao) {
      bateriaForm.resetField("elemento");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [equipamento]);

  if (isEdicao && loadingBateria) {
    return (
      <Box display="flex" justifyContent="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <PageHeader
        title={
          isEdicao ? "Editar Pontos da Bateria" : "Nova Bateria de Calibração"
        }
      />

      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {CALIBRACAO_STEPS.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {/* ---- Step 1: Dados da Bateria ---- */}
      {activeStep === 0 && (
        <Paper variant="outlined" sx={{ p: 3, maxWidth: 560 }}>
          <Stack spacing={2} component="form" onSubmit={handleCriarBateria}>
            <TextField
              select
              label="Equipamento"
              {...bateriaForm.register("equipamento")}
              error={!!bateriaForm.formState.errors.equipamento}
              helperText={bateriaForm.formState.errors.equipamento?.message}
              defaultValue={equipamentoInicial ?? "AA"}
            >
              {EQUIPAMENTOS.map((eq) => (
                <MenuItem key={eq.value} value={eq.value}>
                  {eq.label}
                </MenuItem>
              ))}
            </TextField>

            <TextField
              select
              label="Elemento"
              {...bateriaForm.register("elemento")}
              error={!!bateriaForm.formState.errors.elemento}
              helperText={bateriaForm.formState.errors.elemento?.message}
              defaultValue=""
            >
              {elementosFiltrados.map((el) => (
                <MenuItem key={el} value={el}>
                  {ELEMENTO_LABEL[el]}
                </MenuItem>
              ))}
            </TextField>

            {/* Campos condicionais */}
            {REQUER_VOLUMES.includes(bateriaForm.watch("equipamento")) && (
              <>
                <TextField
                  label="Volume de Solo (dm³)"
                  type="text"
                  inputProps={{
                    inputMode: "decimal",
                    pattern: "[0-9]*[.,]?[0-9]*",
                  }}
                  {...bateriaForm.register("volume_solo", {
                    setValueAs: (value) =>
                      normalizeDecimalOptional(String(value)),
                  })}
                  error={!!bateriaForm.formState.errors.volume_solo}
                  helperText={bateriaForm.formState.errors.volume_solo?.message}
                />
                <TextField
                  label="Volume de Extrator (mL)"
                  type="text"
                  inputProps={{
                    inputMode: "decimal",
                    pattern: "[0-9]*[.,]?[0-9]*",
                  }}
                  {...bateriaForm.register("volume_extrator", {
                    setValueAs: (value) =>
                      normalizeDecimalOptional(String(value)),
                  })}
                  error={!!bateriaForm.formState.errors.volume_extrator}
                  helperText={
                    bateriaForm.formState.errors.volume_extrator?.message
                  }
                />
              </>
            )}

            {REQUER_BRANCO.includes(bateriaForm.watch("equipamento")) && (
              <TextField
                label="Leitura do Branco"
                type="text"
                inputProps={{
                  inputMode: "decimal",
                  pattern: "[0-9]*[.,]?[0-9]*",
                }}
                {...bateriaForm.register("leitura_branco", {
                  setValueAs: (value) =>
                    normalizeDecimalOptional(String(value)),
                })}
                error={!!bateriaForm.formState.errors.leitura_branco}
                helperText={
                  bateriaForm.formState.errors.leitura_branco?.message
                }
              />
            )}

            <FormControlLabel
              control={
                <Switch defaultChecked {...bateriaForm.register("ativo")} />
              }
              label="Marcar como bateria ativa"
            />

            <Button
              type="submit"
              variant="contained"
              disabled={submittingBateria}
              startIcon={
                submittingBateria ? <CircularProgress size={16} /> : null
              }
            >
              {submittingBateria ? "Criando..." : "Criar Bateria"}
            </Button>
          </Stack>
        </Paper>
      )}

      {/* ---- Step 2: Pontos de Calibração ---- */}
      {activeStep === 1 && (
        <Box>
          {/* Titulação / pH-metro: sem curva de calibração */}
          {SEM_CURVA_CALIBRACAO.includes(equipamento) ? (
            <Paper variant="outlined" sx={{ p: 3, maxWidth: 560 }}>
              <Typography variant="body1" mb={2}>
                Este equipamento não utiliza curva de calibração.
              </Typography>
              <Button
                variant="contained"
                onClick={handleFinalizar}
                disabled={salvandoPontos}
              >
                {salvandoPontos ? "Salvando..." : "Concluir"}
              </Button>
            </Paper>
          ) : (
            <Box>
              {isEdicao && bateria && (
                <Paper variant="outlined" sx={{ p: 3, mb: 3, maxWidth: 560 }}>
                  <Typography variant="subtitle2" mb={2}>
                    Parametros da bateria
                  </Typography>
                  <Stack spacing={2}>
                    {REQUER_VOLUMES.includes(equipamento) && (
                      <>
                        <TextField
                          label="Volume de Solo (dm³)"
                          type="text"
                          inputProps={{
                            inputMode: "decimal",
                            pattern: "[0-9]*[.,]?[0-9]*",
                          }}
                          value={parametros.volume_solo}
                          onChange={(e) =>
                            setParametros((prev) => ({
                              ...prev,
                              volume_solo: normalizeDecimalInput(
                                e.target.value,
                              ),
                            }))
                          }
                        />
                        <TextField
                          label="Volume de Extrator (mL)"
                          type="text"
                          inputProps={{
                            inputMode: "decimal",
                            pattern: "[0-9]*[.,]?[0-9]*",
                          }}
                          value={parametros.volume_extrator}
                          onChange={(e) =>
                            setParametros((prev) => ({
                              ...prev,
                              volume_extrator: normalizeDecimalInput(
                                e.target.value,
                              ),
                            }))
                          }
                        />
                      </>
                    )}
                    {REQUER_BRANCO.includes(equipamento) && (
                      <TextField
                        label="Leitura do Branco"
                        type="text"
                        inputProps={{
                          inputMode: "decimal",
                          pattern: "[0-9]*[.,]?[0-9]*",
                        }}
                        value={parametros.leitura_branco}
                        onChange={(e) =>
                          setParametros((prev) => ({
                            ...prev,
                            leitura_branco: normalizeDecimalInput(
                              e.target.value,
                            ),
                          }))
                        }
                      />
                    )}
                    <Button
                      variant="outlined"
                      onClick={() =>
                        atualizarBateria({
                          volume_solo:
                            parametros.volume_solo.trim() === ""
                              ? null
                              : Number(parametros.volume_solo),
                          volume_extrator:
                            parametros.volume_extrator.trim() === ""
                              ? null
                              : Number(parametros.volume_extrator),
                          leitura_branco:
                            parametros.leitura_branco.trim() === ""
                              ? null
                              : Number(parametros.leitura_branco),
                        })
                      }
                      disabled={salvandoParametros}
                      startIcon={
                        salvandoParametros ? (
                          <CircularProgress size={16} />
                        ) : null
                      }
                    >
                      {salvandoParametros ? "Salvando..." : "Salvar parametros"}
                    </Button>
                  </Stack>
                </Paper>
              )}
              {/* Equação ao vivo (edição) */}
              {bateria && (
                <Paper
                  variant="outlined"
                  sx={{ p: 2, mb: 3, bgcolor: "background.default" }}
                >
                  <Stack
                    direction="row"
                    spacing={3}
                    alignItems="center"
                    flexWrap="wrap"
                  >
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Equação atual
                      </Typography>
                      <Typography
                        variant="body2"
                        fontFamily="monospace"
                        fontWeight={600}
                      >
                        {bateria.equacao_formada}
                      </Typography>
                    </Box>
                    {bateria.r_quadrado !== null && (
                      <Box>
                        <Typography variant="caption" color="text.secondary">
                          R²
                        </Typography>
                        <Box>
                          <Chip
                            size="small"
                            label={Number(bateria.r_quadrado).toFixed(4)}
                            color={
                              Number(bateria.r_quadrado) >= 0.99
                                ? "success"
                                : "warning"
                            }
                          />
                        </Box>
                      </Box>
                    )}
                  </Stack>
                </Paper>
              )}

              {/* Pontos já cadastrados (modo edição) */}
              {isEdicao && bateria && bateria.pontos.length > 0 && (
                <>
                  <Typography variant="subtitle2" mb={1}>
                    Pontos cadastrados
                  </Typography>
                  <Table
                    size="small"
                    sx={{ mb: 2, maxWidth: 560 }}
                    aria-label="Pontos cadastrados"
                  >
                    <TableHead>
                      <TableRow>
                        <TableCell>#</TableCell>
                        <TableCell>Concentração (padrão)</TableCell>
                        <TableCell>{leituraLabel}</TableCell>
                        <TableCell align="center">Remover</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {bateria.pontos.map((ponto, i) => (
                        <TableRow key={ponto.id}>
                          <TableCell>{i + 1}</TableCell>
                          <TableCell>{ponto.concentracao}</TableCell>
                          <TableCell>{ponto.absorvancia}</TableCell>
                          <TableCell align="center">
                            <Tooltip title="Remover ponto">
                              <IconButton
                                size="small"
                                color="error"
                                onClick={() => removerPonto(ponto.id)}
                                aria-label={`Remover ponto ${i + 1}`}
                              >
                                <DeleteOutlineIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                  <Divider sx={{ mb: 3 }} />
                </>
              )}

              {/* Grade de novos pontos */}
              <Typography variant="subtitle2" mb={1}>
                Adicionar novos pontos
              </Typography>
              <Table
                size="small"
                sx={{ mb: 1, maxWidth: 560 }}
                aria-label="Novos pontos"
              >
                <TableHead>
                  <TableRow>
                    <TableCell>Concentração (padrão)</TableCell>
                    <TableCell>{leituraLabel}</TableCell>
                    <TableCell width={48} />
                  </TableRow>
                </TableHead>
                <TableBody>
                  {linhas.map((linha, i) => (
                    <TableRow key={i}>
                      <TableCell sx={{ py: 0.5 }}>
                        <TextField
                          value={linha.concentracao}
                          onChange={(e) =>
                            handleAtualizarLinha(
                              i,
                              "concentracao",
                              normalizeDecimalInput(e.target.value),
                            )
                          }
                          type="text"
                          inputProps={{
                            inputMode: "decimal",
                            pattern: "[0-9]*[.,]?[0-9]*",
                          }}
                          size="small"
                          error={!!linha.erro}
                          placeholder="0.0000"
                          sx={{ width: 150 }}
                        />
                      </TableCell>
                      <TableCell sx={{ py: 0.5 }}>
                        <TextField
                          value={linha.absorvancia}
                          onChange={(e) =>
                            handleAtualizarLinha(
                              i,
                              "absorvancia",
                              normalizeDecimalInput(e.target.value),
                            )
                          }
                          type="text"
                          inputProps={{
                            inputMode: "decimal",
                            pattern: "[0-9]*[.,]?[0-9]*",
                          }}
                          size="small"
                          error={!!linha.erro}
                          helperText={linha.erro ?? undefined}
                          placeholder="0.0000"
                          sx={{ width: 150 }}
                        />
                      </TableCell>
                      <TableCell sx={{ py: 0.5 }}>
                        <Tooltip title="Remover linha">
                          <IconButton
                            size="small"
                            onClick={() => handleRemoverLinha(i)}
                            aria-label={`Remover linha ${i + 1}`}
                          >
                            <DeleteOutlineIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              <Button
                size="small"
                startIcon={<AddIcon />}
                onClick={() => handleAdicionarLinhas(1)}
                sx={{ mb: 3 }}
              >
                Adicionar linha
              </Button>

              <Box display="flex" gap={2}>
                {!isEdicao && (
                  <Button variant="text" onClick={() => setActiveStep(0)}>
                    Voltar
                  </Button>
                )}
                <Button
                  variant="contained"
                  onClick={handleFinalizar}
                  disabled={salvandoPontos}
                >
                  {salvandoPontos ? "Salvando..." : "Concluir Calibração"}
                </Button>
              </Box>
            </Box>
          )}
        </Box>
      )}
    </Box>
  );
}
