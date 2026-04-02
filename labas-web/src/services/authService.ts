/**
 * Serviço de autenticação do LABAS.
 *
 * Centraliza todas as chamadas HTTP relacionadas à identidade do usuário:
 * login, renovação de token e cadastro de novos clientes.
 *
 * Princípio aplicado (SOLID — S):
 * Este serviço tem uma única responsabilidade — comunicação com os endpoints
 * de autenticação da API. A lógica de estado (guardar tokens, redirecionar)
 * pertence ao AuthContext, nunca a este arquivo.
 */

import { api } from "./api";
import type {
  LoginPayload,
  TokenPair,
  RegisterPayload,
  AuthUser,
} from "../types/auth";

/**
 * Realiza o login do usuário.
 *
 * Envia as credenciais para `POST /api/token/` e recebe o par de tokens JWT.
 * Quem chama este método (AuthContext) é responsável por armazenar
 * os tokens retornados no localStorage.
 *
 * @returns TokenPair — { access, refresh }
 */
const login = (data: LoginPayload) => api.post<TokenPair>("token/", data);

/**
 * Renova o access token usando o refresh token armazenado.
 *
 * Chamado pelo interceptor de response em `api.ts` quando recebe um 401.
 * Em uso normal, o desenvolvedor não precisa chamar este método diretamente.
 *
 * @returns Novo access token — { access }
 */
const refresh = (refreshToken: string) =>
  api.post<{ access: string }>("token/refresh/", { refresh: refreshToken });

/**
 * Registra um novo cliente (produtor rural) no sistema.
 *
 * Apenas usuários do tipo cliente podem se auto-cadastrar.
 * Contas de staff são criadas pelo administrador no Django Admin.
 *
 * @returns AuthUser — dados do usuário recém-criado
 */
const register = (data: RegisterPayload) =>
  api.post<AuthUser>("register/", data);

/**
 * Busca os dados do usuário autenticado no momento.
 *
 * Usado pelo AuthContext na inicialização da aplicação para restaurar
 * a sessão a partir de um access token válido já salvo no localStorage.
 *
 * @returns AuthUser — { id, username, email, is_staff }
 */
const me = () => api.get<AuthUser>("me/");

export const authService = { login, refresh, register, me };
