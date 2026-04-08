'use client'

import { useState } from 'react'
import { uploadDocument, analyzeDocument } from '@/lib/api'
import { FieldInfo } from '@/types'

interface UploadStepProps {
  onSuccess: (documentId: string, fields: FieldInfo[], sections?: { id: string; name: string }[]) => void
}

export default function UploadStep({ onSuccess }: UploadStepProps) {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [status, setStatus] = useState<string>('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      if (!selectedFile.name.endsWith('.docx')) {
        setError('Apenas arquivos DOCX são suportados')
        return
      }
      setFile(selectedFile)
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Por favor, selecione um arquivo')
      return
    }

    setLoading(true)
    setError(null)

    try {
      console.log('Iniciando upload do arquivo...')
      setStatus('Enviando arquivo...')
      // 1. Upload do arquivo
      const uploadResponse = await uploadDocument(file)
      console.log('Upload concluído:', uploadResponse.document_id)
      
      console.log('Iniciando análise do documento...')
      setStatus('Analisando documento...')
      // 2. Analisar documento
      const analysisResponse = await analyzeDocument(uploadResponse.document_id)
      console.log('Análise concluída:', analysisResponse.total_fields, 'campos encontrados')
      
      setStatus('Concluído!')
      // 3. Chamar callback com sucesso
      const sections = Array.isArray(analysisResponse.sections) && analysisResponse.sections.length > 0 && typeof analysisResponse.sections[0] === 'object'
        ? analysisResponse.sections as { id: string; name: string }[]
        : undefined
      onSuccess(uploadResponse.document_id, analysisResponse.fields, sections)
    } catch (err: any) {
      console.error('Erro ao processar documento:', err)
      
      // Mensagem de erro mais detalhada
      let errorMessage = 'Erro ao processar documento'
      
      if (err.response) {
        // Erro do backend
        errorMessage = err.response.data?.detail || err.response.data?.message || errorMessage
        
        // Mensagens específicas
        if (errorMessage.includes('OPENAI_API_KEY')) {
          errorMessage = 'API Key da OpenAI não configurada. Configure no arquivo backend/.env'
        } else if (errorMessage.includes('rate limit')) {
          errorMessage = 'Limite de requisições atingido. Aguarde alguns minutos e tente novamente.'
        } else if (errorMessage.includes('quota')) {
          errorMessage = 'Cota da OpenAI esgotada. Verifique sua conta OpenAI.'
        } else if (errorMessage.includes('model')) {
          errorMessage = 'Erro com o modelo da OpenAI. Verifique a configuração.'
        }
      } else if (err.request) {
        // Erro de conexão ou timeout
        if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
          errorMessage = 'Tempo de espera esgotado. A análise está demorando muito. Tente novamente ou verifique se o backend está respondendo.'
        } else {
          errorMessage = 'Não foi possível conectar ao servidor. Verifique se o backend está rodando em http://localhost:8000'
        }
      } else {
        // Outro erro
        errorMessage = err.message || errorMessage
      }
      
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-primary-600 mb-4">
          Enviar Contrato
        </h2>
        <p className="text-subtitle mb-6">
          Faça upload do arquivo DOCX do contrato para análise automática dos campos.
        </p>
      </div>

      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-500 transition-colors">
        <input
          type="file"
          accept=".docx"
          onChange={handleFileChange}
          className="hidden"
          id="file-upload"
          disabled={loading}
        />
        <label
          htmlFor="file-upload"
          className="cursor-pointer flex flex-col items-center"
        >
          <svg
            className="w-12 h-12 text-gray-400 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          <span className="text-gray-600 font-medium">
            {file ? file.name : 'Clique para selecionar arquivo DOCX'}
          </span>
          <span className="text-sm text-gray-500 mt-2">
            Apenas arquivos .docx são suportados
          </span>
        </label>
      </div>

      {status && loading && (
        <div className="bg-primary-50 border border-primary-200 text-primary-700 px-4 py-3 rounded-lg">
          <div className="flex items-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{status}</span>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Processando...' : 'Enviar e Analisar'}
      </button>
    </div>
  )
}
