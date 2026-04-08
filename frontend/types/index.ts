export type FieldType = 
  | 'text'
  | 'number'
  | 'currency'
  | 'date'
  | 'cpf'
  | 'cnpj'
  | 'cep'
  | 'phone'
  | 'email'
  | 'select'
  | 'textarea'

export interface FieldInfo {
  field_id: string
  label: string
  type: FieldType
  required: boolean
  original_text: string
  context: string
  placeholder?: string
  section?: string
  section_id?: string
  options?: string[]
  mask?: string
  found_in_document?: boolean
}

export interface AnalysisResponse {
  document_id: string
  fields: FieldInfo[]
  sections: string[] | { id: string; name: string }[]
  total_fields: number
  validation?: {
    valid: boolean
    missing: string[]
    extra: string[]
    found: string[]
  }
}

export interface UploadResponse {
  document_id: string
  filename: string
  message: string
}

export interface FillResponse {
  filled_document_id: string
  message: string
}
