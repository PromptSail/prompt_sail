import { Flex, Spin, Typography } from 'antd';
import HeaderContainer from '../../components/HeaderContainer/HeaderContainer';
import Container from '../../components/Container/Container';
import { useGetConfig, useGetPortfolio } from '../../api/queries';
import Page404 from '../../components/errorPages/page404';
import ProjectsCosts from './ProjectsCosts';
import useGetRangeDatesAndGranularity from '../../hooks/useGetRangeDatesAndGranularity';
import TagCosts from './TagCosts';
const { Title, Text, Paragraph } = Typography;

const Portfolio: React.FC = () => {
    const portfolioDetails = useGetPortfolio();
    const config = useGetConfig();
    const { params, RangeAndGranularity } = useGetRangeDatesAndGranularity();
    if (portfolioDetails.isLoading || config.isLoading)
        return (
            <div className="w-full h-full relative">
                <Spin
                    size="large"
                    className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                />
            </div>
        );
    if (portfolioDetails.isError || config.isError) return <Page404 />;
    if (portfolioDetails.isSuccess && config.isSuccess) {
        const data = portfolioDetails.data;
        const orgName = config.data.data.organization;
        return (
            <Flex gap={24} vertical>
                <HeaderContainer>
                    <div className="my-auto z-10">
                        <Title level={1} className="h4 m-auto">
                            {orgName} portfolio
                        </Title>
                    </div>
                </HeaderContainer>
                <Flex className="px-[24px] max-w-[1600px] w-full mx-auto" gap={12} vertical>
                    <Container>
                        <Flex className="divide-x divide-solid divide-[#F0F0F0]">
                            <div className="border-0 pe-[24px]">
                                <Paragraph className="!mb-1 text-Text/colorTextDescription">
                                    Total projects
                                </Paragraph>
                                <Text className="text-Text/colorText">{data.projects.length}</Text>
                            </div>
                            <div className="border-0 pe-[24px]">
                                <Paragraph className="!mb-1 text-Text/colorTextDescription">
                                    Total transactions
                                </Paragraph>
                                <Text className="text-Text/colorText">
                                    {data.total_transactions}
                                </Text>
                            </div>
                            <div className="border-0 ps-[24px]">
                                <Paragraph className="!mb-1 text-Text/colorTextDescription">
                                    Total cost
                                </Paragraph>
                                <Text className="text-Text/colorText">
                                    $ {data.total_cost.toFixed(4)}
                                </Text>
                            </div>
                        </Flex>
                    </Container>
                    <Container>
                        <Flex justify="space-between">
                            <Title level={2} className="h5 my-auto !mb-1">
                                Statistics
                            </Title>
                            {RangeAndGranularity}
                        </Flex>
                        <div>
                            <ProjectsCosts dateParams={params} />
                        </div>
                        <div>
                            <TagCosts dateParams={params} />
                        </div>
                    </Container>
                </Flex>
            </Flex>
        );
    }
};

export default Portfolio;
