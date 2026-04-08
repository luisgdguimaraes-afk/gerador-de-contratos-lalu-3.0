// Declaração de tipos para react-input-mask
declare module 'react-input-mask' {
  import * as React from 'react';

  export interface Props extends React.InputHTMLAttributes<HTMLInputElement> {
    /**
     * Mask string. Format characters:
     * 9: 0-9
     * a: A-Z, a-z
     * *: A-Z, a-z, 0-9
     */
    mask: string | Array<string | RegExp>;
    
    /**
     * Character to cover unfilled parts of the mask
     */
    maskChar?: string | null;
    
    /**
     * Show mask when input is empty and has no focus
     */
    alwaysShowMask?: boolean;
    
    /**
     * Use inputRef instead of ref if you need input node to manage focus, selection, etc.
     */
    inputRef?: React.Ref<HTMLInputElement>;
    
    /**
     * In case you need to implement more complex masking behavior, you can provide
     * beforeMaskedValueChange function to change masked value and cursor position
     * before it will be applied to the input.
     */
    beforeMaskedValueChange?: (
      newState: BeforeMaskedValueChangeState,
      oldState: BeforeMaskedValueChangeState,
      userInput: string,
      maskOptions: MaskOptions
    ) => BeforeMaskedValueChangeState;
  }

  export interface BeforeMaskedValueChangeState {
    value: string;
    selection: Selection | null;
  }

  export interface Selection {
    start: number;
    end: number;
  }

  export interface MaskOptions {
    mask: string | Array<string | RegExp>;
    maskChar: string;
    alwaysShowMask: boolean;
    formatChars: { [key: string]: string };
    permanents: number[];
  }

  export default class InputMask extends React.Component<Props> {}
}
