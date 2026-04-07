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
import type { Laudo, LaudoPayload } from "../types/analise";

const buildDefaultValues = (laudo: Laudo): LaudoFormInput => ({
  cliente_codigo: laudo.cliente.codigo,
  data_emissao: laudo.data_emissao,
  data_saida: laudo.data_saida ?? "",
  observacoes: laudo.observacoes ?? "",
});

export function useLaudoEditForm(laudo?: Laudo) {
  const navigate = useNavigate();
  const { showSuccess, showApiError } = useSnackbar();
  const [submitting, setSubmitting] = useState(false);

  const form = useForm<LaudoFormInput, unknown, LaudoForm>({
    resolver: zodResolver(laudoSchema),
    defaultValues: {
      cliente_codigo: "",
      data_emissao: "",
      data_saida: "",
      observacoes: "",
    },
  });

  useEffect(() => {
    if (!laudo) return;
    form.reset(buildDefaultValues(laudo));
  }, [laudo, form]);

  const onSubmit = form.handleSubmit(async (data) => {
    if (!laudo) return;
    setSubmitting(true);
    try {
      const payload: Partial<LaudoPayload> = {
        cliente_codigo: data.cliente_codigo,
        data_emissao: data.data_emissao,
        data_saida: data.data_saida || null,
        observacoes: data.observacoes || undefined,
      };
      await laudoService.atualizar(laudo.id, payload);
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
        if (!hasFieldError) showApiError(err);
        return;
      }
      showApiError(err);
    } finally {
      setSubmitting(false);
    }
  });

  return { form, submitting, onSubmit };
}
