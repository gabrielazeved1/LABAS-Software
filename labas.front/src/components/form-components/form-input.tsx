import { useRef, useState } from "react";
import { Control } from "react-hook-form";
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from "../ui/form";
import { Input } from "../ui/input";
import { Eye, EyeOff } from "lucide-react";
import VMasker from "vanilla-masker";


interface Props extends React.ComponentProps<"input"> {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  control: Control<any>;
  label?: string;
  name: string;
  placeholder?: string;
  description?: string;
  rules?: {
    required?: boolean | string,
    pattern?: RegExp;
  };
  mask?: string;
  disabled?: boolean;
  isAutoCapitalize?: boolean;
  isLowerCase?: boolean;
}

export function FormInput({
  control,
  label,
  name,
  placeholder,
  description,
  rules,
  disabled,
  mask,
  type,
  isLowerCase,
  isAutoCapitalize,
  ...props
}: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [showPassword, setShowPassword] = useState(false);

  const isPassword = type === "password";
  const inputType = isPassword ? (showPassword ? "text" : "password") : type;

  const applyMask = (value: string) => {
    if (!mask) return value;
    return VMasker.toPattern(value, mask);
  };

   const capitalizeWords = (text: string) =>
    text.replace(/\b\w/g, (char) => char.toUpperCase());

  return (
    <FormField
      control={control}   
      name={name}
      rules={rules}
      disabled={disabled}
      render={({ field }) => (
        <FormItem className="w-full h-fit">
          {label && (
            <FormLabel>
              {label}
              {props?.required && <span className="text-red-500">*</span>}
            </FormLabel>
          )}
          <FormControl>
            <div className="relative">
              <Input
                className={`${props.readOnly
                    ? "bg-gray-100 text-gray-500 cursor-default border-transparent"
                    : ""
                  } ${props.className ?? ""} [&::-webkit-calendar-picker-indicator]:hidden pr-10`}

                  
                placeholder={placeholder ?? "Insira um valor"}
                {...props}
                {...field}
                ref={inputRef}
                type={inputType}
                value={applyMask(field.value ?? "")}
                onChange={(e) => {
                  let value = applyMask(e.target.value);
                  
                  if (isLowerCase) {
                    value = value.toLowerCase();
                  }

                  if (isAutoCapitalize) {
                    value = capitalizeWords(value);
                  }

                  field.onChange(value);
                }}
                />
              {isPassword && (
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500"
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              )}
              
            </div>
          </FormControl>
          {description && <FormDescription>{description}</FormDescription>}
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
