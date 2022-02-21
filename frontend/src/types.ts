export interface Wallet {
  id: string;
  name: string;
  balance_currency: string;
  native_amount: number;
  native_currency: string;
  balance_amount: number;
}

export interface Price {
  base: string;
  currency: string;
  amount: number;
}
