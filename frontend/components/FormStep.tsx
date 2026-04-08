'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { FieldInfo } from '@/types'
import DynamicField from './DynamicField'

/** Agrupamento das seções em etapas do formulário */
const FORM_STEPS = [
  { title: 'Comprador', shortTitle: 'Comprador', sectionIds: ['COMPRADOR_PF', 'COMPRADOR_PJ'] },
  { title: 'Unidade e Valores', shortTitle: 'Unidade', sectionIds: ['UNIDADE', 'PRECO', 'COMISSAO'] },
  { title: 'Imobiliária e Corretor', shortTitle: 'Imob. e Corretor', sectionIds: ['IMOBILIARIA', 'CORRETOR'] },
  { title: 'Bem e Parcelas', shortTitle: 'Bem e Parcelas', sectionIds: ['BEM', 'PARCELAS'] },
  { title: 'Assinatura', shortTitle: 'Assinatura', sectionIds: ['ASSINATURA', 'TESTEMUNHAS'] },
]

interface FormStepProps {
  fields: FieldInfo[]
  sections: { id: string; name: string }[]
  onSubmit: (formData: Record<string, any>) => void
  isLoading?: boolean
}

export default function FormStep({ fields, sections, onSubmit, isLoading = false }: FormStepProps) {
  const [error, setError] = useState<string | null>(null)
  const [buyerType, setBuyerType] = useState<'PF' | 'PJ'>('PF')
  const [formStepIndex, setFormStepIndex] = useState(0)
  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm()

  const scrollToTop = () => {
    if (typeof window !== 'undefined') {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  // Filtrar campos baseado no tipo de comprador
  const filteredFields = fields.filter(field => {
    if (field.section_id === 'COMPRADOR_PF' && buyerType !== 'PF') return false
    if (field.section_id === 'COMPRADOR_PJ' && buyerType !== 'PJ') return false
    return true
  })

  // Agrupar campos por seção
  const fieldsBySection = sections
    ? sections.map(section => ({
        ...section,
        fields: filteredFields.filter(f => f.section_id === section.id)
      })).filter(section => section.fields.length > 0)
    : filteredFields.reduce((acc, field) => {
        const section = field.section || 'Outros'
        if (!acc[section]) acc[section] = []
        acc[section].push(field)
        return acc
      }, {} as Record<string, FieldInfo[]>)

  const currentStep = FORM_STEPS[formStepIndex]
  const currentSectionIds = currentStep?.sectionIds ?? []
  const isArray = Array.isArray(fieldsBySection)

  // Seções a exibir na etapa atual (ordenadas conforme FORM_STEPS)
  let sectionsToShow: { id: string; name: string; fields: FieldInfo[] }[] = isArray
    ? (fieldsBySection as { id: string; name: string; fields: FieldInfo[] }[]).filter(
        s => currentSectionIds.includes(s.id)
      )
    : (Object.entries(fieldsBySection as Record<string, FieldInfo[]>).filter(([id]) =>
        currentSectionIds.includes(id)
      ) as [string, FieldInfo[]][]).map(([id, sectionFields]) => ({
        id,
        name: id,
        fields: sectionFields
      }))
  sectionsToShow.sort((a, b) => currentSectionIds.indexOf(a.id) - currentSectionIds.indexOf(b.id))

  const isFirstStep = formStepIndex === 0
  const isLastStep = formStepIndex === FORM_STEPS.length - 1
  const hasCompradorSections = fields.some(f => f.section_id === 'COMPRADOR_PF') || fields.some(f => f.section_id === 'COMPRADOR_PJ')

  const onSubmitForm = async (data: Record<string, any>) => {
    setError(null)
    try {
      onSubmit(data)
    } catch (err: any) {
      setError(err.message || 'Erro ao processar formulário')
    }
  }

  const goNext = () => {
    if (!isLastStep) {
      setFormStepIndex(i => i + 1)
      scrollToTop()
    }
  }

  const goPrev = () => {
    if (!isFirstStep) {
      setFormStepIndex(i => i - 1)
      scrollToTop()
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-primary-600 mb-2">
          Preencher Campos
        </h2>

        {/* Stepper: indicador de etapas */}
        <div className="flex flex-wrap items-center justify-center gap-1 sm:gap-2 mb-6 py-3 px-2 bg-gray-50 rounded-lg">
          {FORM_STEPS.map((step, i) => {
            const isActive = i === formStepIndex
            const isPast = i < formStepIndex
            return (
              <div key={step.title} className="flex items-center">
                <div
                  className={`
                    flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium shrink-0
                    ${isActive ? 'bg-primary-600 text-white ring-2 ring-primary-300' : ''}
                    ${isPast ? 'bg-green-500 text-white' : ''}
                    ${!isActive && !isPast ? 'bg-gray-300 text-gray-500' : ''}
                  `}
                >
                  {isPast ? '✓' : i + 1}
                </div>
                <span
                  className={`
                    ml-1.5 text-sm font-medium hidden sm:inline
                    ${isActive ? 'text-primary-700' : isPast ? 'text-green-700' : 'text-gray-500'}
                  `}
                >
                  {step.shortTitle}
                </span>
                {i < FORM_STEPS.length - 1 && (
                  <div className={`w-4 sm:w-6 h-0.5 mx-1 sm:mx-2 ${isPast ? 'bg-green-400' : 'bg-gray-300'}`} />
                )}
              </div>
            )
          })}
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-6">
        {/* Seletor de tipo de comprador — só na etapa 1 quando existir */}
        {isFirstStep && hasCompradorSections && (
          <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tipo de Comprador
            </label>
            <div className="flex gap-4">
              <label className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  value="PF"
                  checked={buyerType === 'PF'}
                  onChange={() => setBuyerType('PF')}
                  className="mr-2"
                />
                <span>Pessoa Física</span>
              </label>
              <label className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  value="PJ"
                  checked={buyerType === 'PJ'}
                  onChange={() => setBuyerType('PJ')}
                  className="mr-2"
                />
                <span>Pessoa Jurídica</span>
              </label>
            </div>
          </div>
        )}

        {/* Campos da etapa atual */}
        {sectionsToShow.map((section) => (
          <div key={section.id} className="border border-gray-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-primary-600 mb-4 pb-2 border-b">
              {section.name}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {section.fields.map((field) => (
                <DynamicField
                  key={field.field_id}
                  field={field}
                  register={register}
                  errors={errors}
                  setValue={setValue}
                  watch={watch}
                />
              ))}
            </div>
          </div>
        ))}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Navegação entre etapas */}
        <div className="flex gap-3 pt-2">
          {!isFirstStep && (
            <button
              type="button"
              onClick={goPrev}
              className="flex-1 sm:flex-none px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Anterior
            </button>
          )}
          <div className={isFirstStep ? 'w-full' : 'flex-1'} />
          {!isLastStep ? (
            <button
              type="button"
              onClick={goNext}
              className="px-6 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Próximo
            </button>
          ) : (
            <button
              type="submit"
              disabled={isLoading}
              className="px-6 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Gerando contrato...' : 'Gerar Contrato'}
            </button>
          )}
        </div>
      </form>
    </div>
  )
}
