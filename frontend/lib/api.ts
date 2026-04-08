import axios from 'axios'
import { UploadResponse, AnalysisResponse, FillResponse } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutos de timeout
})

// Funções helper para novo fluxo (sem upload)
export const contractApi = {
  // Obter schema do formulário
  getSchema: (templateId?: string) => 
    api.get('/api/schema', { params: { template_id: templateId } }),
  
  // Listar templates disponíveis
  listTemplates: () => 
    api.get('/api/templates'),
  
  // Preencher e gerar contrato
  fillContract: (templateId: string, fields: Record<string, any>, buyerType?: string) => 
    api.post('/api/fill', { template_id: templateId, fields, buyer_type: buyerType }),
  
  // Download do contrato (sempre PDF agora)
  downloadContract: async (documentId: string) => {
    const response = await api.get(`/api/download/${documentId}`, {
      responseType: 'blob',
    })
    return response
  },
}

// Funções legadas (mantidas para compatibilidade futura)
export const uploadDocument = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post<UploadResponse>('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 30000, // 30 segundos para upload
  })

  return response.data
}

export const analyzeDocument = async (documentId: string): Promise<AnalysisResponse> => {
  const response = await api.post<AnalysisResponse>('/api/analyze', {
    document_id: documentId,
  }, {
    timeout: 300000, // 5 minutos para análise
  })

  return response.data
}

export const fillDocument = async (
  documentId: string,
  fields: Record<string, any>
): Promise<FillResponse> => {
  const response = await api.post<FillResponse>('/api/fill', {
    document_id: documentId,
    fields,
  })

  return response.data
}

// Função legada removida - usar contractApi.downloadContract agora
