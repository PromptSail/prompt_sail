import { DownOutlined } from '@ant-design/icons';
import { Button, ConfigProvider, Flex, Input, Popover, Slider, theme } from 'antd';
import { CSSProperties, useEffect, useState } from 'react';

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
    const [display, setDisplay] = useState('');
    const buttonStyles: CSSProperties = {
        border: `1px solid ${token.colorPrimary}`,
        boxShadow: `0 0 0 2px ${token.colorPrimary + '12'}`
    };
    const step = 1 / 10 ** fixed;
    const { start, end } = values;
    const startNull = start == null;
    const endNull = end == null;
    useEffect(() => {
        if (startNull || endNull) setDisplay('');
    }, [values]);
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
                                setDisplay(`${prefix}${v[0]} - ${v[1]}`);
                            }}
                        />
                        <Flex gap={8}>
                            <Input
                                type="number"
                                min={min}
                                max={max}
                                step={step}
                                defaultValue={min}
                                value={startNull ? min : start}
                                onChange={(v) => {
                                    const val = v.target.valueAsNumber;
                                    const min = Number(v.target.min);
                                    if (val >= min || isNaN(val)) {
                                        onChange({ start: val, end: endNull ? max : end });
                                        setDisplay(
                                            `${prefix}${val || startNull ? min : start} - ${
                                                endNull ? max : end
                                            }`
                                        );
                                    }
                                }}
                            />
                            <Input
                                type="number"
                                name="rightInput"
                                min={min}
                                max={max}
                                value={endNull ? max : end}
                                step={step}
                                onChange={(v) => {
                                    const val = v.target.valueAsNumber;
                                    const max = Number(v.target.max);
                                    if (val <= max) {
                                        onChange({ start: startNull ? min : start, end: val });
                                        setDisplay(
                                            `${prefix}${startNull ? min : start} - ${
                                                val || endNull ? max : end
                                            }`
                                        );
                                    }
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
                        {display.length == 0 ? (
                            <span className="w-full text-start opacity-70">Select</span>
                        ) : (
                            <span className="text-start w-full">{display}</span>
                        )}
                        <DownOutlined className="m-auto text-[12px] opacity-70" />
                    </Flex>
                </Button>
            </Popover>
        </ConfigProvider>
    );
};

export default SelectForm;
