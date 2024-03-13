import { FormikValues } from '../types';
import { useState } from 'react';

import ProvidersListCollapse from './ProvidersList';
import ProviderForm from './ProviderForm';
import Container from '../../../pages/Project/Container';
import { Button, Tooltip } from 'antd';

interface Props {
    ProvidersList: typeof FormikValues.ai_providers;
    setProvidersList: (list: typeof FormikValues.ai_providers) => void;
    projectSlug: string;
    isProjects: boolean;
    isError: boolean;
}

const ProviderFormAndList: React.FC<Props> = ({
    ProvidersList,
    setProvidersList,
    projectSlug,
    isProjects,
    isError
}) => {
    const [EditedProvider, setEditedProvider] = useState<number | null>(null);
    const [FormShowed, setFormShow] = useState(!isProjects);
    return (
        <>
            {ProvidersList.length > 0 && (
                <ProvidersListCollapse
                    ProvidersList={ProvidersList}
                    projectSlug={projectSlug}
                    EditedProvider={EditedProvider}
                    setEditedProvider={setEditedProvider}
                    setProvidersList={setProvidersList}
                    setFormShow={setFormShow}
                />
            )}
            {FormShowed && (
                <Container
                    header="Provider details"
                    classname={isError ? '!border-red-500' : ''}
                    desc={
                        <>
                            <span className={isError ? 'text-red-500 font-bold' : ''}>
                                Add at least one AI provider
                            </span>
                            , to use PromptSail as a proxy server for collecting{' '}
                            <Tooltip
                                placement="top"
                                title="A transaction consists of a request sent to an LLM provider
                                                    and a response received to the request"
                            >
                                <span className="underline font-bold">transactions</span>
                            </Tooltip>{' '}
                            in the project
                        </>
                    }
                >
                    <ProviderForm
                        EditedProvider={EditedProvider}
                        ProvidersList={ProvidersList}
                        setProvidersList={setProvidersList}
                        setEditedProvider={setEditedProvider}
                        slug={projectSlug}
                        setFormShow={setFormShow}
                    />
                </Container>
            )}
            {!FormShowed && !EditedProvider && (
                <Button
                    type="primary"
                    ghost
                    block
                    onClick={() => {
                        setFormShow(true);
                        setEditedProvider(null);
                    }}
                >
                    Add another AI Provider
                </Button>
            )}
        </>
    );
};
export default ProviderFormAndList;
