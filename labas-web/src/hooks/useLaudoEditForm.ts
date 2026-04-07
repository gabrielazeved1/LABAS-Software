import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import type { FieldPath } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import {
  laudoSchema,
  type LaudoForm,
  type LaudoFormInput,
} from "../schemas/laudoSchemas";
import { laudoService } from "../services/laudoService";
import { useSnackbar } from "./useSnackbar";
import type { AnaliseSolo, AnaliseSoloPayload } from "../types/analise";

const numericField = (value: number | null): number | "" =>
  value === null ? "" : value;

const buildDefaultValues = (laudo: AnaliseSolo): LaudoFormInput => ({
  n_lab: laudo.n_lab,
  cliente_codigo: laudo.cliente.codigo,
  data_entrada: laudo.data_entrada,
  data_saida: laudo.data_saida ?? "",
  ph_agua: numericField(laudo.ph_agua),
  ph_cacl2: numericField(laudo.ph_cacl2),
  ph_kcl: numericField(laudo.ph_kcl),
  p_m: numericField(laudo.p_m),
  p_r: numericField(laudo.p_r),
  p_rem: numericField(laudo.p_rem),
  mo: numericField(laudo.mo),
  s: numericField(laudo.s),
  b: numericField(laudo.b),
  k: numericField(laudo.k),
  na: numericField(laudo.na),
  ca: numericField(laudo.ca),
  mg: numericField(laudo.mg),
  cu: numericField(laudo.cu),
  fe: numericField(laudo.fe),
  mn: numericField(laudo.mn),
  zn: numericField(laudo.zn),
  al: numericField(laudo.al),
  h_al: numericField(laudo.h_al),
  areia: numericField(laudo.areia),
  argila: numericField(laudo.argila),
  silte: numericField(laudo.silte),
});

const normalizePayload = (data: LaudoForm): Partial<AnaliseSoloPayload> => {
  const entries = Object.entries(data).map(([key, value]) => [
    key,
    value === undefined || value === "" ? null : value,
  ]);
  return Object.fromEntries(entries) as Partial<AnaliseSoloPayload>;
};

export function useLaudoEditForm(laudo?: AnaliseSolo) {
  const navigate = useNavigate();
  const { showSuccess, showApiError } = useSnackbar();
  const [submitting, setSubmitting] = useState(false);

  const form = useForm<LaudoFormInput, unknown, LaudoForm>({
    resolver: zodResolver(laudoSchema),
    defaultValues: {
      n_lab: "",
      cliente_codigo: "",
      data_entrada: "",
      data_saida: "",
    },
  });

  // Popula o formulário quando o laudo for carregado assincronamente
  useEffect(() => {
    if (!laudo) return;
    form.reset(buildDefaultValues(laudo));
  }, [laudo, form]);

  const onSubmit = form.handleSubmit(async (data) => {
    if (!laudo) return;
    setSubmitting(true);
    try {
      await laudoService.atualizar(laudo.n_lab, normalizePayload(data));
      showSuccess("Laudo atualizado com sucesso.");
      navigate("/laudos");
    } catch (err) {
      const responseData = (err as { response?: { data?: unknown } })?.response
        ?.data;
      if (responseData && typeof responseData === "object") {
        let hasFieldError = false;
        (
          Object.entries(responseData as Record<string, unknown>) as [
            FieldPath<LaudoFormInput>,
            unknown,
          ][]
        ).forEach(([field, msgs]) => {
          const message = Array.isArray(msgs) ? msgs[0] : String(msgs);
          if (message && field in laudoSchema.shape) {
            form.setError(field, { type: "server", message });
            hasFieldError = true;
          }
        });
        if (!hasFieldError) {
          showApiError(err);
        }
        return;
      }
      showApiError(err);
    } finally {
      setSubmitting(false);
    }
  });

  return { form, submitting, onSubmit };
}
