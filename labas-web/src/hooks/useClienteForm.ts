import { useCallback, useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { clienteService } from "../services/clienteService";
import { clienteSchema } from "../schemas/clienteSchemas";
import { useSnackbar } from "./useSnackbar";
import type {
  ClienteSchemaInput,
  ClienteSchemaOutput,
} from "../schemas/clienteSchemas";
import type { Cliente } from "../types/cliente";

interface UseClienteFormOptions {
  /** Se fornecido, o formulário opera em modo edição. */
  clienteInicial?: Cliente;
  onSucesso?: (cliente: Cliente) => void;
}

export function useClienteForm({
  clienteInicial,
  onSucesso,
}: UseClienteFormOptions = {}) {
  const [loading, setLoading] = useState(false);
  const { showSuccess, showApiError } = useSnackbar();
  const edicao = !!clienteInicial;

  const form = useForm<ClienteSchemaInput, unknown, ClienteSchemaOutput>({
    resolver: zodResolver(clienteSchema),
    defaultValues: {
      codigo: clienteInicial?.codigo ?? "",
      nome: clienteInicial?.nome ?? "",
      telefone: clienteInicial?.telefone ?? "",
      email: clienteInicial?.email ?? "",
      municipio: clienteInicial?.municipio ?? "",
      area: clienteInicial?.area ?? "",
      observacoes: clienteInicial?.observacoes ?? "",
    },
  });

  // Quando clienteInicial chegar (após fetch assíncrono), popula o formulário
  useEffect(() => {
    if (!clienteInicial) return;
    form.reset({
      codigo: clienteInicial.codigo,
      nome: clienteInicial.nome,
      telefone: clienteInicial.telefone ?? "",
      email: clienteInicial.email ?? "",
      municipio: clienteInicial.municipio ?? "",
      area: clienteInicial.area ?? "",
      observacoes: clienteInicial.observacoes ?? "",
    });
  }, [clienteInicial, form]);

  const onSubmit = useCallback(
    async (values: ClienteSchemaOutput) => {
      setLoading(true);
      try {
        let salvo: Cliente;
        if (edicao && clienteInicial) {
          salvo = await clienteService.atualizar(clienteInicial.codigo, values);
          showSuccess("Cliente atualizado com sucesso.");
        } else {
          salvo = await clienteService.criar(values);
          showSuccess("Cliente criado com sucesso.");
        }
        onSucesso?.(salvo);
      } catch (err) {
        showApiError(err);
      } finally {
        setLoading(false);
      }
    },
    [clienteInicial, edicao, onSucesso, showApiError, showSuccess],
  );

  return { form, loading, edicao, onSubmit: form.handleSubmit(onSubmit) };
}
