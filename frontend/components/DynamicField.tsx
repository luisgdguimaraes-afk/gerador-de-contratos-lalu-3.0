'use client'

import { FieldInfo } from '@/types'
import { UseFormRegister, FieldErrors, UseFormSetValue, UseFormWatch } from 'react-hook-form'
import InputMask from 'react-input-mask'

interface DynamicFieldProps {
  field: FieldInfo
  register: UseFormRegister<any>
  errors: FieldErrors
  setValue: UseFormSetValue<any>
  watch: UseFormWatch<any>
}

export default function DynamicField({
  field,
  register,
  errors,
  setValue,
  watch,
}: DynamicFieldProps) {
  const fieldError = errors[field.field_id]

  const getInputType = () => {
    switch (field.type) {
      case 'email':
        return 'email'
      case 'number':
      case 'currency':
        return 'number'
      case 'date':
        return 'date'
      default:
        return 'text'
    }
  }

  const getMask = () => {
    // Se o campo tem mask definida, usar ela
    if (field.mask) {
      return field.mask
    }
    
    switch (field.type) {
      case 'cpf':
        return '999.999.999-99'
      case 'cnpj':
        return '99.999.999/9999-99'
      case 'cep':
        return '99999-999'
      case 'phone':
        return '(99) 99999-9999'
      case 'currency':
        return undefined // Será tratado separadamente
      default:
        return undefined
    }
  }

  const formatCurrency = (value: string) => {
    // Remove tudo que não é número
    const numbers = value.replace(/\D/g, '')
    // Converte para formato de moeda
    const formatted = (parseInt(numbers) / 100).toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    })
    return formatted
  }

  const handleCurrencyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    const numbers = value.replace(/\D/g, '')
    setValue(field.field_id, numbers)
  }

  const currencyValue = watch(field.field_id)
  const displayCurrency = currencyValue
    ? formatCurrency(currencyValue)
    : ''

  if (field.type === 'currency') {
    return (
      <div>
        <label htmlFor={field.field_id} className="label-field">
          {field.label}
          {field.required && <span className="text-red-500 ml-1">*</span>}
        </label>
        <input
          type="text"
          id={field.field_id}
          {...register(field.field_id, {
            required: field.required ? 'Campo obrigatório' : false,
          })}
          onChange={handleCurrencyChange}
          value={displayCurrency}
          placeholder={field.placeholder || 'R$ 0,00'}
          className="input-field"
        />
        {fieldError && (
          <p className="text-red-500 text-sm mt-1">
            {fieldError.message as string}
          </p>
        )}
        {field.context && (
          <p className="text-gray-500 text-xs mt-1 italic">
            Contexto: {field.context.substring(0, 100)}...
          </p>
        )}
      </div>
    )
  }

  const mask = getMask()

  // Renderizar campo SELECT
  if (field.type === 'select' && field.options) {
    return (
      <div>
        <label htmlFor={field.field_id} className="label-field">
          {field.label}
          {field.required && <span className="text-red-500 ml-1">*</span>}
        </label>
        <select
          id={field.field_id}
          className="input-field"
          {...register(field.field_id, {
            required: field.required ? 'Campo obrigatório' : false,
          })}
        >
          <option value="">Selecione...</option>
          {field.options.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
        {fieldError && (
          <p className="text-red-500 text-sm mt-1">
            {fieldError.message as string}
          </p>
        )}
      </div>
    )
  }

  // Renderizar campo TEXTAREA
  if (field.type === 'textarea') {
    return (
      <div className="md:col-span-2">
        <label htmlFor={field.field_id} className="label-field">
          {field.label}
          {field.required && <span className="text-red-500 ml-1">*</span>}
        </label>
        <textarea
          id={field.field_id}
          rows={4}
          placeholder={field.placeholder || ''}
          className="input-field"
          {...register(field.field_id, {
            required: field.required ? 'Campo obrigatório' : false,
          })}
        />
        {fieldError && (
          <p className="text-red-500 text-sm mt-1">
            {fieldError.message as string}
          </p>
        )}
      </div>
    )
  }

  // Renderizar campos normais (text, number, date, etc.)
  return (
    <div>
      <label htmlFor={field.field_id} className="label-field">
        {field.label}
        {field.required && <span className="text-red-500 ml-1">*</span>}
      </label>
      {mask ? (
        <InputMask
          mask={mask}
          id={field.field_id}
          type={getInputType()}
          placeholder={field.placeholder || ''}
          className="input-field"
          {...register(field.field_id, {
            required: field.required ? 'Campo obrigatório' : false,
          })}
        />
      ) : (
        <input
          id={field.field_id}
          type={getInputType()}
          placeholder={field.placeholder || ''}
          className="input-field"
          {...register(field.field_id, {
            required: field.required ? 'Campo obrigatório' : false,
          })}
        />
      )}
      {fieldError && (
        <p className="text-red-500 text-sm mt-1">
          {fieldError.message as string}
        </p>
      )}
      {field.context && (
        <p className="text-gray-500 text-xs mt-1 italic">
          Contexto: {field.context.substring(0, 100)}...
        </p>
      )}
    </div>
  )
}
