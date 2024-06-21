import { DownOutlined } from '@ant-design/icons';
import { Button, ConfigProvider, Flex, Input, Popover, Slider, theme } from 'antd';
import { CSSProperties, useState } from 'react';

const { useToken } = theme;

interface Props {
    values: {
        start: number | null;
        end: number | null;
    };
    min?: number;
    max?: number;
    onChange: (obj: { start: number; end: number }) => void;
    prefix?: string;
    fixed?: number;
}

const SelectForm: React.FC<Props> = ({
    values,
    onChange,
    prefix = '',
    min = 0,
    max = 100,
    fixed = 1
}) => {
    const { token } = useToken();
    const [isOpen, setOpen] = useState(false);
    const [inputs, setInputs] = useState({ start: `${min}`, end: `${max}` });
    const pattern = /^[0-9]+([.,][0-9]*)?$/;
    const buttonStyles: CSSProperties = {
        border: `1px solid ${token.colorPrimary}`,
        boxShadow: `0 0 0 2px ${token.colorPrimary + '12'}`
    };
    const step = 1 / 10 ** fixed;
    const { start, end } = values;
    const startNull = start == null;
    const endNull = end == null;
    const inputsBlur = () => {
        let start: string | number = inputs.start;
        let end: string | number = inputs.end;
        start = Math.min(Math.max(Number(start.replace(',', '.')), min), max);
        end = Math.min(Math.max(Number(end.replace(',', '.')), min), max);
        setInputs({ start: `${start}`, end: `${end}` });
        onChange({ start, end });
    };
    return (
        <ConfigProvider wave={{ disabled: true }}>
            <Popover
                className="w-full"
                placement="bottom"
                content={
                    <Flex vertical gap={7}>
                        <Slider
                            className="my-0"
                            range
                            defaultValue={[min, max]}
                            min={min}
                            max={max}
                            value={[startNull ? min : start, endNull ? max : end]}
                            step={step}
                            onChange={(v) => {
                                onChange({ start: v[0], end: v[1] });
                                setInputs({ start: `${v[0]}`, end: `${v[1]}` });
                            }}
                        />
                        <Flex gap={8}>
                            <Input
                                type="text"
                                className="max-w-[100px]"
                                min={min}
                                max={max}
                                step={step}
                                defaultValue={min}
                                value={inputs.start}
                                onBlur={() => inputsBlur()}
                                onChange={(v) => {
                                    setInputs((prevState) => ({
                                        ...prevState,
                                        start: (() => {
                                            let value = '';
                                            value =
                                                !v.target.value.length ||
                                                pattern.test(v.target.value)
                                                    ? v.target.value
                                                    : prevState.start;
                                            onChange({
                                                start: Number(value.replace(',', '.')),
                                                end: Number(inputs.end)
                                            });
                                            return value;
                                        })()
                                    }));
                                }}
                            />
                            <Input
                                type="text"
                                className="max-w-[100px]"
                                min={min}
                                max={max}
                                value={inputs.end}
                                step={step}
                                onBlur={() => inputsBlur()}
                                onChange={(v) => {
                                    setInputs((prevState) => ({
                                        ...prevState,
                                        end: (() => {
                                            let value = '';
                                            value =
                                                !v.target.value.length ||
                                                pattern.test(v.target.value)
                                                    ? v.target.value
                                                    : prevState.start;
                                            onChange({
                                                start: Number(inputs.start),
                                                end: Number(value.replace(',', '.'))
                                            });
                                            return value;
                                        })()
                                    }));
                                }}
                            />
                        </Flex>
                    </Flex>
                }
                trigger="click"
                onOpenChange={setOpen}
            >
                <Button style={isOpen ? buttonStyles : {}} className="px-[11px]">
                    <Flex>
                        {inputs.start == `${min}` && inputs.end == `${max}` ? (
                            <span className="w-full text-start opacity-70">Select</span>
                        ) : (
                            <span className="text-start w-full">{`${prefix}${inputs.start} - ${inputs.end}`}</span>
                        )}
                        <DownOutlined className="m-auto text-[12px] opacity-70" />
                    </Flex>
                </Button>
            </Popover>
        </ConfigProvider>
    );
};

export default SelectForm;
