import { DownOutlined } from '@ant-design/icons';
import { Button, ConfigProvider, Flex, Input, Popover, Slider, theme } from 'antd';
import { CSSProperties, useState } from 'react';

const { useToken } = theme;

interface Props {
    values: {
        start: number;
        end: number;
    };
    min?: number;
    max?: number;
    onChange: (obj: { start: number; end: number }) => void;
    prefix?: string;
}

const SelectForm: React.FC<Props> = ({ values, onChange, prefix = '', min = 0, max = 100 }) => {
    const { token } = useToken();
    const [isOpen, setOpen] = useState(false);
    const [display, setDisplay] = useState('');
    const buttonStyles: CSSProperties = {
        border: `1px solid ${token.colorPrimary}`,
        boxShadow: `0 0 0 2px ${token.colorPrimary + '12'}`
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
                            defaultValue={[values.start, values.end]}
                            min={min}
                            max={max}
                            value={[values.start, values.end]}
                            step={max / 100}
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
                                step={max / 100}
                                value={values.start}
                                onChange={(v) => {
                                    const val = v.target.valueAsNumber;
                                    const min = Number(v.target.min);
                                    // console.log(val);
                                    if (val >= min || isNaN(val)) {
                                        onChange({ start: val, end: values.end });
                                        setDisplay(
                                            `${prefix}${val || values.start} - ${values.end}`
                                        );
                                    }
                                }}
                            />
                            <Input
                                type="number"
                                name="rightInput"
                                min={min}
                                max={max}
                                value={values.end}
                                step={max / 100}
                                onChange={(v) => {
                                    const val = v.target.valueAsNumber;
                                    const max = Number(v.target.max);
                                    if (val <= max) {
                                        onChange({ start: values.start, end: val });
                                        setDisplay(
                                            `${prefix}${values.start} - ${val || values.end}`
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
