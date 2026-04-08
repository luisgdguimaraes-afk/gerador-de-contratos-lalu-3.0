'use client'

import { useState } from 'react'
import { contractApi } from '@/lib/api'

interface DownloadInfo {
  id: string
  name: string
  download_id: string
}

interface DownloadStepProps {
  // Documento principal (compatibilidade com versões antigas)
  documentId: string
  onReset: () => void
  // Lista de documentos retornados pelo backend (quando disponível)
  documents?: DownloadInfo[]
}

export default function DownloadStep({ documentId, onReset, documents }: DownloadStepProps) {
  const [downloadingId, setDownloadingId] = useState<string | null>(null)

  // Sempre há dois documentos: Quadro Resumo (contrato principal) e Condições Gerais
  // O botão principal já baixa o Quadro Resumo, então só precisamos mostrar o botão das Condições Gerais
  const getCondicoesGeraisId = (): string | null => {
    // Se o backend retornou a lista de documentos, usar o ID correto
    if (documents && documents.length > 0) {
      const condicoesDoc = documents.find(doc => doc.id === 'condicoes_gerais')
      if (condicoesDoc) {
        return condicoesDoc.download_id
      }
    }

    // Tentar inferir o ID das Condições Gerais a partir do documentId
    // O documentId pode ser: <uuid>_quadro_resumo ou apenas <uuid>
    const quadroSuffix = '_quadro_resumo'
    if (documentId.endsWith(quadroSuffix)) {
      const baseId = documentId.slice(0, -quadroSuffix.length)
      return `${baseId}_condicoes_gerais`
    }

    // Se o documentId é um UUID completo, construir o ID das condições gerais
    const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i
    const match = documentId.match(uuidPattern)
    if (match) {
      const baseUuid = match[0]
      return `${baseUuid}_condicoes_gerais`
    }

    // Última tentativa: assumir que o documentId é o UUID base
    return `${documentId}_condicoes_gerais`
  }

  const condicoesGeraisId = getCondicoesGeraisId()

  const handleDownload = async (downloadId: string, filenamePrefix: string) => {
    try {
      setDownloadingId(downloadId)
      console.log(`[DOWNLOAD] Iniciando download de: ${downloadId}`)
      
      const response = await contractApi.downloadContract(downloadId)
      console.log(`[DOWNLOAD] Resposta recebida:`, response.status, response.headers)
      
      // Criar blob e fazer download
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${filenamePrefix}_${downloadId.slice(0, 8)}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      console.log(`[DOWNLOAD] Download concluído com sucesso`)
      
    } catch (error: any) {
      console.error('[DOWNLOAD] Erro ao baixar:', error)
      console.error('[DOWNLOAD] Status:', error.response?.status)
      console.error('[DOWNLOAD] Dados:', error.response?.data)
      console.error('[DOWNLOAD] Download ID usado:', downloadId)
      alert(`Erro ao baixar o arquivo. Tente novamente.\n\nDetalhes: ${error.response?.data?.detail || error.message}`)
    } finally {
      setDownloadingId(null)
    }
  }

  return (
    <div className="text-center py-8">
      <div className="mb-6">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-primary-600 mb-2">
          Contrato Gerado com Sucesso!
        </h2>
        <p className="text-subtitle">
          Seu contrato está pronto para download em formato PDF.
        </p>
      </div>

      <div className="space-y-4">
        {/* Botão principal (compatibilidade): sempre disponível */}
        <button
          onClick={() => handleDownload(documentId, 'contrato')}
          disabled={downloadingId !== null}
          className="w-full max-w-xs mx-auto bg-primary-600 text-white py-3 px-6 rounded-lg 
                     hover:bg-primary-700 disabled:bg-gray-400 transition-colors
                     flex items-center justify-center gap-2"
        >
          {downloadingId === documentId ? (
            <>
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Baixando...
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Baixar Contrato (PDF)
            </>
          )}
        </button>

        {/* Botão para Condições Gerais (sempre disponível, pois sempre há dois documentos) */}
        {condicoesGeraisId && (
          <div className="max-w-xs mx-auto">
            <button
              onClick={() => handleDownload(condicoesGeraisId, 'condicoes_gerais')}
              disabled={downloadingId !== null}
              className="w-full bg-white border border-primary-600 text-primary-600 py-2.5 px-4 rounded-lg 
                         hover:bg-primary-50 disabled:bg-gray-100 disabled:border-gray-300 disabled:text-gray-400
                         text-sm font-medium flex items-center justify-center gap-2"
            >
              {downloadingId === condicoesGeraisId ? (
                <>
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Baixando...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Condições Gerais
                </>
              )}
            </button>
          </div>
        )}

        <button
          onClick={onReset}
          className="w-full max-w-xs mx-auto bg-gray-200 text-gray-700 py-3 px-6 rounded-lg 
                     hover:bg-gray-300 transition-colors"
        >
          Gerar Novo Contrato
        </button>
      </div>

      <p className="mt-6 text-sm text-gray-500">
        O contrato foi gerado em formato PDF para garantir que a formatação 
        seja mantida em qualquer dispositivo ou programa.
      </p>
    </div>
  )
}
