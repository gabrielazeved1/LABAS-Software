import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import {
  laudoSchema,
  type LaudoForm,
  type LaudoFormInput,
} from "../schemas/laudoSchemas";
import { laudoService } from "../services/laudoService";
import { useSnackbar } from "./useSnackbar";
import type { AnaliseSoloPayload } from "../types/analise";

const getTodayISO = () => new Date().toISOString().slice(0, 10);

const normalizePayload = (data: LaudoForm): AnaliseSoloPayload => {
  const entries = Object.entries(data).map(([key, value]) => [
    key,
    value === undefined || value === "" ? null : value,
  ]);

  return Object.fromEntries(entries) as AnaliseSoloPayload;
};

export function useLaudoForm() {
  const navigate = useNavigate();
  const { showSuccess, showApiError } = useSnackbar();
  const [submitting, setSubmitting] = useState(false);

  const form = useForm<LaudoFormInput, unknown, LaudoForm>({
    resolver: zodResolver(laudoSchema),
    defaultValues: {
      n_lab: "",
      cliente_codigo: "",
      data_entrada: getTodayISO(),
      data_saida: "",
    },
  });

  const onSubmit = form.handleSubmit(async (data) => {
    setSubmitting(true);
    try {
      await laudoService.criar(normalizePayload(data));
      showSuccess("Laudo criado com sucesso.");
      navigate("/laudos");
    } catch (err) {
      showApiError(err);
    } finally {
      setSubmitting(false);
    }
  });

  return {
    form,
    submitting,
    onSubmit,
  };
}
