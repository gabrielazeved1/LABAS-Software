// src/utils/whatsapp.ts

/**
 * Remove os caracteres especiais do telefone e gera o link direto do WhatsApp com a mensagem pronta.
 */
export const gerarLinkWhatsApp = (
  telefone: string,
  laudoId: string | number,
  nomeCliente: string,
): string => {
  // Regex para remover parênteses, espaços e traços, mantendo apenas números
  const numeroLimpo = telefone.replace(/\D/g, "");

  // Mensagem padrão e profissional
  const mensagem = `Olá, ${nomeCliente}. O seu laudo técnico (Nº ${laudoId}) referente à análise de solo já está disponível. Segue o documento em anexo:`;

  // Codifica a string para o formato de URL (substituindo espaços por %20, etc.)
  const mensagemCodificada = encodeURIComponent(mensagem);

  // Assume o DDI 55 (Brasil) por padrão
  return `https://wa.me/55${numeroLimpo}?text=${mensagemCodificada}`;
};
