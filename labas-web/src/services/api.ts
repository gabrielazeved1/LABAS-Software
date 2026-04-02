/**
 * Módulo central de comunicação HTTP do LABAS.
 *
 * Regra de ouro: toda chamada à API Django deve passar por esta instância.
 * Nunca use `fetch` ou `axios.create` diretamente em componentes ou hooks.
 *
 * Responsabilidades deste módulo:
 * 1. Criar a instância Axios com a baseURL configurável por variável de ambiente
 * 2. Injetar o Bearer token JWT em todas as requisições autenticadas (interceptor de request)
 * 3. Renovar automaticamente o access token quando expirado — código 401 (interceptor de response)
 * 4. Rejeitar a requisição e limpar os tokens quando o refresh também falhar
 */

import axios from "axios";

/**
 * Instância Axios configurada para a API do LABAS.
 *
 * A baseURL é lida da variável de ambiente `VITE_API_BASE_URL` (definida no `.env`).
 * Em caso de ausência da variável, utiliza o endereço local padrão do backend Django.
 */
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/",
  headers: { "Content-Type": "application/json" },
});

// ─── Interceptor de Request ───────────────────────────────────────────────────

/**
 * Injeta o Bearer token JWT em todas as requisições que partirem desta instância.
 *
 * O token é lido do localStorage a cada requisição, garantindo que qualquer
 * renovação feita pelo interceptor de response seja refletida imediatamente.
 */
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ─── Interceptor de Response ──────────────────────────────────────────────────

/**
 * Trata automaticamente erros 401 (token expirado) tentando renovar o access token
 * com o refresh token armazenado no localStorage.
 *
 * Fluxo de renovação:
 * 1. Requisição retorna 401
 * 2. Marca a requisição original com `_retry = true` para evitar loop infinito
 * 3. Faz POST em `token/refresh/` com o refresh token
 * 4. Atualiza o access token no localStorage
 * 5. Re-executa a requisição original com o novo token
 *
 * Se o refresh token também estiver expirado ou ausente:
 * - Remove ambos os tokens do localStorage (força o logout)
 * - Rejeita a Promise — o AuthContext detecta e redireciona para /login
 */
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh_token");

      if (refreshToken) {
        try {
          const { data } = await api.post<{ access: string }>(
            "token/refresh/",
            { refresh: refreshToken },
          );

          // Atualiza o token no storage e na requisição que falhou
          localStorage.setItem("access_token", data.access);
          originalRequest.headers.Authorization = `Bearer ${data.access}`;

          // Re-executa a requisição original com o novo access token
          return api(originalRequest);
        } catch {
          // Refresh token inválido ou expirado — limpa a sessão
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
        }
      }
    }

    return Promise.reject(error);
  },
);
