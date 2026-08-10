// src/contexts/SnackbarContext.tsx
import { createContext, useCallback, useEffect, useState, type ReactNode } from "react";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";

// ---------------------------------------------------------------------------
// Tipos
// ---------------------------------------------------------------------------

type Severity = "success" | "error" | "warning" | "info";

export interface SnackbarContextValue {
  /** Exibe uma mensagem de sucesso */
  showSuccess: (message: string) => void;
  /** Exibe uma mensagem de erro */
  showError: (message: string) => void;
  /** Exibe uma mensagem de aviso */
  showWarning: (message: string) => void;
  /** Exibe uma mensagem informativa */
  showInfo: (message: string) => void;
  /**
   * Extrai e exibe o erro de uma resposta da API Django.
   *
   * O backend retorna erros no formato:
   *   { campo: ["mensagem"] }  → erro de validação (400)
   *   { detail: "mensagem" }   → erro geral (403, 404, etc.)
   *
   * Este helper normaliza os dois formatos para uma string legível.
   */
  showApiError: (error: unknown) => void;
}

// ---------------------------------------------------------------------------
// Contexto
// ---------------------------------------------------------------------------

export const SnackbarContext = createContext<SnackbarContextValue | null>(null);

// ---------------------------------------------------------------------------
// Provider
// ---------------------------------------------------------------------------

const AUTO_HIDE_MS = 4000;

type QueueItem = { message: string; severity: Severity };

export function SnackbarProvider({ children }: { children: ReactNode }) {
  const [queue, setQueue] = useState<QueueItem[]>([]);
  const [current, setCurrent] = useState<QueueItem | null>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open && queue.length > 0) {
      const [next, ...rest] = queue;
      setCurrent(next);
      setQueue(rest);
      setOpen(true);
    }
  }, [open, queue]);

  const show = useCallback((message: string, severity: Severity) => {
    setQueue((prev) => [...prev, { message, severity }]);
  }, []);

  const showSuccess = useCallback(
    (message: string) => show(message, "success"),
    [show],
  );

  const showError = useCallback(
    (message: string) => show(message, "error"),
    [show],
  );

  const showWarning = useCallback(
    (message: string) => show(message, "warning"),
    [show],
  );

  const showInfo = useCallback(
    (message: string) => show(message, "info"),
    [show],
  );

  const showApiError = useCallback(
    (error: unknown) => {
      // Tenta extrair a mensagem do formato de erro do Django REST Framework
      const data = (error as { response?: { data?: unknown } })?.response?.data;

      if (data && typeof data === "object") {
        // Formato: { detail: "string" } → erros gerais (403, 404...)
        if (
          "detail" in data &&
          typeof (data as Record<string, unknown>).detail === "string"
        ) {
          show((data as Record<string, string>).detail, "error");
          return;
        }

        // Formato: { campo: ["msg1", "msg2"] } → erros de validação (400)
        const messages = Object.entries(data as Record<string, unknown>)
          .flatMap(([field, msgs]) => {
            const list = Array.isArray(msgs) ? msgs : [msgs];
            return list.map((m) => `${field}: ${m}`);
          })
          .join(" | ");

        if (messages) {
          show(messages, "error");
          return;
        }
      }

      // Fallback genérico
      show("Ocorreu um erro inesperado. Tente novamente.", "error");
    },
    [show],
  );

  const handleClose = (_: unknown, reason?: string) => {
    if (reason === "clickaway") return;
    setOpen(false);
  };

  return (
    <SnackbarContext.Provider
      value={{ showSuccess, showError, showWarning, showInfo, showApiError }}
    >
      {children}

      <Snackbar
        open={open}
        autoHideDuration={AUTO_HIDE_MS}
        onClose={handleClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={() => setOpen(false)}
          severity={current?.severity ?? "info"}
          variant="filled"
          sx={{ width: "100%" }}
        >
          {current?.message}
        </Alert>
      </Snackbar>
    </SnackbarContext.Provider>
  );
}
