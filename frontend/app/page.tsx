'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import FormStep from '@/components/FormStep'
import DownloadStep from '@/components/DownloadStep'
import { FieldInfo } from '@/types'
import { contractApi } from '@/lib/api'

interface SchemaResponse {
  template_id: string
  template_name: string
  fields: FieldInfo[]
  sections: { id: string; name: string }[]
  total_fields: number
}

type Step = 'form' | 'download'

export default function Home() {
  const [step, setStep] = useState<Step>('form')
  const [schema, setSchema] = useState<SchemaResponse | null>(null)
  const [filledDocumentId, setFilledDocumentId] = useState<string | null>(null)
  const [generatedDocuments, setGeneratedDocuments] = useState<any[] | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Carregar schema ao iniciar
  useEffect(() => {
    loadSchema()
  }, [])

  const loadSchema = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const response = await contractApi.getSchema()
      setSchema(response.data)
    } catch (err: any) {
      setError('Erro ao carregar formulário. Tente novamente.')
      console.error('Erro ao carregar schema:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleFormSubmit = async (formData: Record<string, any>) => {
    try {
      setIsLoading(true)
      setError(null)
      
      // Filtrar campos vazios antes de enviar
      const filteredData = Object.fromEntries(
        Object.entries(formData).filter(([_, value]) => 
          value !== null && value !== undefined && value !== ''
        )
      )
      
      // Detectar tipo de comprador baseado nos campos preenchidos
      const hasPF = Object.keys(filteredData).some(key => key.startsWith('COMPRADOR_PF_'))
      const hasPJ = Object.keys(filteredData).some(key => key.startsWith('COMPRADOR_PJ_'))
      const buyerType = hasPF && !hasPJ ? 'PF' : hasPJ && !hasPF ? 'PJ' : 'PF' // Default para PF
      
      console.log('Enviando dados:', filteredData)
      console.log('Tipo de comprador detectado:', buyerType)
      
      const response = await contractApi.fillContract(
        schema?.template_id || 'rota_do_sol',
        filteredData,
        buyerType
      )
      
      // ID principal (usado para compatibilidade) e lista de documentos retornados
      console.log('[PAGE] Resposta do fill:', response.data)
      console.log('[PAGE] filled_document_id:', response.data.filled_document_id)
      console.log('[PAGE] documents:', response.data.documents)
      console.log('[PAGE] documents_count:', response.data.documents_count)
      
      setFilledDocumentId(response.data.filled_document_id)
      setGeneratedDocuments(response.data.documents || null)
      setStep('download')
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Erro ao gerar contrato. Verifique os dados e tente novamente.'
      setError(errorMessage)
      console.error('Erro ao gerar contrato:', err)
      console.error('Detalhes do erro:', err.response?.data)
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewContract = () => {
    setFilledDocumentId(null)
    setGeneratedDocuments(null)
    setStep('form')
  }

  // Tela de loading inicial
  if (isLoading && !schema) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-primary-50 to-[#fdfcf9] flex items-center justify-center">
        <div className="text-center">
          <Image
            src="/logo-lalu.png"
            alt="LALU - Administradora de Bens"
            width={140}
            height={100}
            className="mx-auto mb-6 object-contain"
          />
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-subtitle">Carregando formulário...</p>
        </div>
      </main>
    )
  }

  // Tela de erro
  if (error && !schema) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-primary-50 to-[#fdfcf9] flex items-center justify-center">
        <div className="text-center bg-white rounded-xl shadow-lg p-8 max-w-md">
          <Image
            src="/logo-lalu.png"
            alt="LALU - Administradora de Bens"
            width={140}
            height={100}
            className="mx-auto mb-6 object-contain"
          />
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={loadSchema}
            className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Tentar Novamente
          </button>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-primary-50 to-[#fdfcf9] py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <Image
              src="/logo-lalu.png"
              alt="LALU - Administradora de Bens"
              width={180}
              height={130}
              className="mx-auto mb-6 object-contain"
            />
            <h1 className="text-3xl font-bold text-primary-600 mb-2">
              Gerador de Contratos
            </h1>
            <p className="text-subtitle">
              {schema?.template_name || 'Residencial Rota do Sol'}
            </p>
          </div>

          {/* Progress Indicator */}
          <div className="flex items-center justify-center mb-8">
            <div className="flex items-center">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                step === 'form' ? 'bg-primary-600 text-white' : 'bg-green-500 text-white'
              }`}>
                {step === 'download' ? '✓' : '1'}
              </div>
              <span className="ml-2 font-medium">Preencher Dados</span>
            </div>
            <div className="w-16 h-1 bg-gray-300 mx-4">
              <div className={`h-full transition-all ${step === 'download' ? 'bg-green-500 w-full' : 'bg-gray-300 w-0'}`}></div>
            </div>
            <div className="flex items-center">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                step === 'download' ? 'bg-primary-600 text-white' : 'bg-gray-300 text-gray-500'
              }`}>
                2
              </div>
              <span className={`ml-2 font-medium ${step === 'download' ? '' : 'text-gray-400'}`}>
                Download
              </span>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          {/* Content */}
          {step === 'form' && schema && (
            <FormStep
              fields={schema.fields}
              sections={schema.sections}
              onSubmit={handleFormSubmit}
              isLoading={isLoading}
            />
          )}

          {step === 'download' && filledDocumentId && (
            <DownloadStep
              documentId={filledDocumentId}
              documents={generatedDocuments || undefined}
              onReset={handleNewContract}
            />
          )}
        </div>
      </div>
    </main>
  )
}
