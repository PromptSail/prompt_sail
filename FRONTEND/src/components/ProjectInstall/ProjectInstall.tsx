import { useState } from 'react';
import { Button, Modal } from 'react-bootstrap';
import SyntaxHighlighter from 'react-syntax-highlighter';
import * as styles from 'react-syntax-highlighter/dist/esm/styles/hljs';

interface Props {
    slug: string;
    api_base: string;
}

const ProjectInstall: React.FC<Props> = ({ slug, api_base }) => {
    const [isShow, setShow] = useState(false);
    return (
        <>
            <Button variant="secondary" onClick={() => setShow((e) => !e)}>
                Install
            </Button>
            <Modal size="lg" show={isShow} onHide={() => setShow((e) => !e)}>
                <Modal.Header closeButton>
                    <Modal.Title className="text-3xl font-semibold">Installation</Modal.Title>
                </Modal.Header>
                <Modal.Body className="flex flex-col gap-3">
                    <div>
                        <SyntaxHighlighter
                            language="python"
                            style={styles.atomOneDark}
                            customStyle={{ display: 'inline' }}
                        >{`http://${slug}.promptsail.local`}</SyntaxHighlighter>
                        <span className="hidden md:inline">&rArr;</span>
                        <span className="block md:hidden my-5 ms-3">&dArr;</span>
                        <SyntaxHighlighter
                            language="python"
                            style={styles.atomOneDark}
                            customStyle={{ display: 'inline' }}
                        >
                            {api_base}
                        </SyntaxHighlighter>
                    </div>
                    <h2 className="text-2xl font-semibold">Usage example</h2>
                    <p>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur rutrum
                        dapibus lorem quis hendrerit. Fusce eu sapien at lacus facilisis tincidunt
                        eu ut quam. Ut quis lectus quis tortor vehicula fermentum vitae id nibh.
                        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
                        inceptos himenaeos. Sed vel tortor eget eros pulvinar blandit.
                    </p>
                    <h4 className="text-xl font-semibold md:text-2xl">Using openai library</h4>
                    <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                        {`import openai openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = "http://${slug}.promptsail.local"
openai.ChatCompletion.create(
model="gpt-3.5-turbo", 
messages=[{"role": "user", "content": "Generate poem made of 2 sentences."}], )`}
                    </SyntaxHighlighter>
                    <h4 className="text-xl font-semibold md:text-2xl">Using langchain library</h4>
                    <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                        {`from langchain.llms import OpenAI
llm = OpenAI(
model_name="text-davinci-003",
openai_api_base="http://${slug}.promptsail.local",
)
llm("Explaining the meaning of life in one sentence")`}
                    </SyntaxHighlighter>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShow((e) => !e)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
};
export default ProjectInstall;
