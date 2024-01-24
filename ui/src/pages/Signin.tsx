import { useFormik } from 'formik';
import { SetStateAction } from 'react';
import { Button, FloatingLabel, Form } from 'react-bootstrap';
import { checkLogin } from '../storage/login';
import Logo from '../assets/imgs/prompt_sail_logo200.jpg';
const Signin: React.FC<{ setLoginState: (arg: SetStateAction<boolean>) => void }> = ({
    setLoginState
}) => {
    const formik = useFormik({
        initialValues: {
            email: '',
            password: ''
        },
        onSubmit: () => {
            localStorage.setItem('login', 'true');
            setLoginState(checkLogin());
        }
    });
    return (
        <>
            <div className="signin">
                <div className="formContainer">
                    <div className="form">
                        <h2>Welcome to Ermlab</h2>
                        <h5>Sign in to continue</h5>
                        <form onSubmit={formik.handleSubmit}>
                            <div className="inputs">
                                <FloatingLabel label="Email">
                                    <Form.Control
                                        type="email"
                                        name="email"
                                        placeholder="email@example.com"
                                        value={formik.values['email']}
                                        onChange={formik.handleChange}
                                        autoComplete="login email"
                                    />
                                </FloatingLabel>
                                <FloatingLabel label="Password">
                                    <Form.Control
                                        type="password"
                                        name="password"
                                        placeholder="$tronGP@s$word"
                                        value={formik.values['password']}
                                        onChange={formik.handleChange}
                                        autoComplete="login current-password"
                                    />
                                </FloatingLabel>
                            </div>
                            <Button type="submit">Log In</Button>
                        </form>
                    </div>
                    <div>
                        <img src={Logo} />
                        <h4>Prompt Sail</h4>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Signin;
