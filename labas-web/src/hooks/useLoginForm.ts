/**
 * Hook customizado para orquestrar o formulário de login.
 * Princípio S (SRP): apenas lógica de submit e estado local.
 * Princípio D (DIP): recebe AuthContext como dependência.
 */
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import type { LoginFormData } from "../validators/loginSchema";
import { loginSchema } from "../validators/loginSchema";

export function useLoginForm(loginFn: (data: LoginFormData) => Promise<void>) {
  const [apiError, setApiError] = useState<string | null>(null);
  const form = useForm<LoginFormData>({ resolver: zodResolver(loginSchema) });

  async function onSubmit(data: LoginFormData) {
    setApiError(null);
    try {
      await loginFn(data);
    } catch (err: unknown) {
      const axiosError = err as {
        response?: { data?: { detail?: string; non_field_errors?: string[] } };
      };
      const detail =
        axiosError?.response?.data?.detail ??
        axiosError?.response?.data?.non_field_errors?.[0] ??
        "Usuário ou senha inválidos.";
      setApiError(detail);
    }
  }

  return { ...form, apiError, setApiError, onSubmit };
}
