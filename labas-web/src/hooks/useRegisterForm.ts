/**
 * Hook customizado para orquestrar o formulário de cadastro (2 steps).
 * Princípio S (SRP): apenas lógica de submit, step e estado local.
 * Princípio D (DIP): recebe dependências (registerFn, loginFn, navigate) via parâmetro.
 */
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import type { Step1Data, Step2Data } from "../validators/registerSchema";
import { step1Schema, step2Schema } from "../validators/registerSchema";

export function useRegisterForm(
  registerFn: (payload: any) => Promise<void>,
  loginFn: (payload: any) => Promise<void>,
  navigate: (path: string, opts?: any) => void,
) {
  const [activeStep, setActiveStep] = useState(0);
  const [step1Data, setStep1Data] = useState<Step1Data | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  const form1 = useForm<Step1Data>({ resolver: zodResolver(step1Schema) });
  const form2 = useForm<Step2Data>({ resolver: zodResolver(step2Schema) });

  function handleStep1Submit(data: Step1Data) {
    setStep1Data(data);
    setActiveStep(1);
  }

  async function handleStep2Submit(data: Step2Data) {
    if (!step1Data) return;
    setApiError(null);
    const payload = {
      username: step1Data.username,
      email: step1Data.email,
      password: step1Data.password,
      nome_cliente: data.nome_cliente,
      codigo_cliente: data.codigo_cliente,
      municipio: data.municipio,
      area: data.area,
    };
    try {
      await registerFn(payload);
      await loginFn({
        username: step1Data.username,
        password: step1Data.password,
      });
      navigate("/dashboard");
    } catch (err: unknown) {
      const axiosError = err as {
        response?: { data?: Record<string, string[]> };
      };
      const errors = axiosError?.response?.data;
      if (errors) {
        const firstMessage = Object.values(errors).flat()[0];
        setApiError(firstMessage ?? "Erro ao criar conta. Tente novamente.");
      } else {
        setApiError("Erro ao criar conta. Tente novamente.");
      }
    }
  }

  return {
    activeStep,
    setActiveStep,
    step1Data,
    apiError,
    setApiError,
    form1,
    form2,
    handleStep1Submit,
    handleStep2Submit,
  };
}
