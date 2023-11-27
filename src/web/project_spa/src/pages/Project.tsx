import { AxiosResponse } from 'axios';
import { useState } from 'react';
import { useQuery } from 'react-query';
import { useParams } from 'react-router-dom';
import { getProjectResponse } from '../api/interfaces';
import api from '../api/api';

const Project: React.FC = () => {
    const params = useParams();
    const [data, setData] = useState({});
    const { isSuccess, isLoading, error } = useQuery('projects', () => {
        api.getProjects() //`${params.projectId || ''}`)
            .then((res) => {
                console.log(res);
                // setData(res);
            })
            .catch((err) => err);
    });
    if (isLoading)
        return (
            <>
                <div>loading...</div>
            </>
        );
    if (error)
        return (
            <>
                <div>An error has occurred</div>
                {console.log(error)}
            </>
        );
    if (isSuccess) return <div></div>;
    // return (
    //     <>
    //         <div className="m-auto mb-5 mt-[100px] max-w-[80%]">
    //             <form
    //                 method="post"
    //                 action="/ui/project/delete"
    //                 onSubmit={() => {
    //                     if (!confirm('Are you sure?')) return false;
    //                 }}
    //                 // onSubmit="if(!confirm('Are you sure?')){return false;}"
    //             >
    //                 <input type="hidden" name="project_id" value="{{ project.id }}" />
    //                 <button type="submit">Delete</button>
    //             </form>
    //             <a href="/ui/project/{{project.id}}/update">
    //                 <button>Edit</button>
    //             </a>
    //             <div>
    //                 <button
    //                     className="btn btn-primary"
    //                     type="button"
    //                     data-bs-toggle="modal"
    //                     data-bs-target="#updateProjectModal"
    //                 >
    //                     Edit
    //                 </button>
    //                 <div
    //                     className="modal fade"
    //                     id="updateProjectModal"
    //                     tabIndex={-1}
    //                     aria-labelledby="updateProjectModalLabel"
    //                     aria-hidden="true"
    //                     data-projectId="{{project.id}}"
    //                 >
    //                     <form>
    //                         <div className="modal-dialog">
    //                             <div className="modal-content">
    //                                 <div className="modal-header">
    //                                     <h1
    //                                         className="modal-title fs-5"
    //                                         id="updateProjectModalLabel"
    //                                     >
    //                                         Edit Project
    //                                     </h1>
    //                                     <button
    //                                         className="btn-close"
    //                                         type="button"
    //                                         data-bs-dismiss="modal"
    //                                         aria-label="Close"
    //                                     ></button>
    //                                 </div>
    //                                 <div className="modal-body">
    //                                     <div className="input-group mb-3">
    //                                         <span className="input-group-text">Name</span>
    //                                         <input
    //                                             className="form-control"
    //                                             type="text"
    //                                             name="name"
    //                                             required
    //                                         />
    //                                     </div>
    //                                     <div className="input-group mb-3">
    //                                         <span className="input-group-text">Slug</span>
    //                                         <input
    //                                             className="form-control"
    //                                             type="text"
    //                                             name="slug"
    //                                             required
    //                                         />
    //                                     </div>
    //                                     <div className="input-group mb-3">
    //                                         <span className="input-group-text">
    //                                             Description
    //                                         </span>
    //                                         <textarea
    //                                             className="form-control"
    //                                             id="description"
    //                                             name="description"
    //                                             rows={4}
    //                                             cols={50}
    //                                             maxLength={280}
    //                                             required
    //                                         ></textarea>
    //                                     </div>
    //                                     <div className="input-group mb-3">
    //                                         {' '}
    //                                         <span className="input-group-text">
    //                                             API Base URL
    //                                         </span>
    //                                         <input
    //                                             className="form-control"
    //                                             type="url"
    //                                             name="api_base"
    //                                             placeholder="https://api.openai.com/v1"
    //                                             required
    //                                         />
    //                                     </div>
    //                                     <div className="input-group mb-3">
    //                                         {' '}
    //                                         <span className="input-group-text">
    //                                             Provider name
    //                                         </span>
    //                                         <select
    //                                             className="form-select"
    //                                             id="provider_name"
    //                                             name="provider_name"
    //                                         >
    //                                             <option value="OpenAI">OpenAI</option>
    //                                             <option value="Azure OpenAI">
    //                                                 Azure OpenAI
    //                                             </option>
    //                                             <option value="Google Palm">Google Palm</option>
    //                                             <option value="Anthropic Cloud">
    //                                                 Anthropic Cloud
    //                                             </option>
    //                                             <option value="Meta LLama">Meta LLama</option>
    //                                             <option value="HuggingFace">HuggingFace</option>
    //                                             <option value="Custom">Custom</option>
    //                                         </select>
    //                                     </div>
    //                                     <div className="input-group mb-3">
    //                                         {' '}
    //                                         <span className="input-group-text">Model name</span>
    //                                         <input
    //                                             className="form-control"
    //                                             type="text"
    //                                             name="model_name"
    //                                             required
    //                                         />
    //                                     </div>
    //                                     <div className="input-group mb-3">
    //                                         <span className="input-group-text">Tags</span>
    //                                         <textarea
    //                                             className="form-control"
    //                                             id="tags"
    //                                             name="tags"
    //                                             rows={4}
    //                                             cols={50}
    //                                             required
    //                                         ></textarea>
    //                                     </div>
    //                                     <div className="input-group mb-3">
    //                                         {' '}
    //                                         <span className="input-group-text">
    //                                             Organization
    //                                         </span>
    //                                         <input
    //                                             className="form-control"
    //                                             type="text"
    //                                             name="org_id"
    //                                         />
    //                                     </div>
    //                                 </div>
    //                                 <div className="modal-footer">
    //                                     <button
    //                                         className="btn btn-secondary"
    //                                         type="button"
    //                                         data-bs-dismiss="modal"
    //                                     >
    //                                         Close
    //                                     </button>
    //                                     <button className="btn btn-primary" type="submit">
    //                                         Sumbit
    //                                     </button>
    //                                 </div>
    //                             </div>
    //                         </div>
    //                     </form>
    //                 </div>
    //             </div>
    //             <h1 className="text-3xl font-semibold text-center mb-5 md:text-5xl">
    //                 {' '}
    //                 data
    //                 {data.name}
    //             </h1>
    //             <h2 className="text-2xl font-semibold mb-2 md:text-4xl">Project details:</h2>
    //             <p className="mb-5">
    //                 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur rutrum
    //                 dapibus lorem quis hendrerit. Fusce eu sapien at lacus facilisis tincidunt
    //                 eu ut quam. Ut quis lectus quis tortor vehicula fermentum vitae id nibh.
    //                 Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
    //                 inceptos himenaeos. Sed vel tortor eget eros pulvinar blandit.
    //             </p>
    //             <p>
    //                 <pre className="mb-5">
    //                     <code className="python" style={{ display: 'inline' }}>
    //                         {/* {{project_url}} */}
    //                     </code>
    //                     <span className="hidden md:inline">&rArr;</span>
    //                     <span className="block md:hidden my-5 ms-3">&dArr;</span>
    //                     <code className="python" style={{ display: 'inline' }}>
    //                         {/* {{project.ai_providers.0.api_base}} */}
    //                     </code>
    //                 </pre>
    //             </p>
    //             <h2 className="text-2xl font-semibold mb-2 md:text-4xl">Usage example</h2>
    //             <p className="mb-5">
    //                 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur rutrum
    //                 dapibus lorem quis hendrerit. Fusce eu sapien at lacus facilisis tincidunt
    //                 eu ut quam. Ut quis lectus quis tortor vehicula fermentum vitae id nibh.
    //                 Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
    //                 inceptos himenaeos. Sed vel tortor eget eros pulvinar blandit.
    //             </p>
    //             <h4 className="text-xl font-semibold mb-2 md:text-2xl">Using openai library</h4>
    //             <pre>
    //                 <code className="python">
    //                     import openai openai.api_key = os.environ["OPENAI_API_KEY"]
    //                     openai.api_base = "{/* {{project_url}} */}"
    //                     openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=
    //                     {/* [{"role": "user", "content": "Generate poem made of 2 sentences."}] */}
    //                     , )
    //                 </code>
    //             </pre>
    //             <h4 className="text-xl font-semibold mb-2 mt-3 md:text-2xl">
    //                 Using langchain library
    //             </h4>
    //             <pre>
    //                 <code className="python">
    //                     from langchain.llms import OpenAI llm = OpenAI(
    //                     model_name="text-davinci-003", openai_api_base="
    //                     {/* {{project_url}} */}
    //                     ", ) llm("Explaining the meaning of life in one sentence")
    //                 </code>
    //             </pre>
    //             <h4 className="text-xl font-semibold mb-2 mt-3 md:text-2xl">
    //                 LLM Transactions
    //             </h4>
    //             <div className="overflow-x-auto p-3"></div>
    //         </div>
    //     </>
    // );
};

export default Project;
