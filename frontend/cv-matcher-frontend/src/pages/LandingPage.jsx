import { Link } from "react-router-dom";
import { useInView } from "react-intersection-observer";
import CountUp from "react-countup";
import StepCard from "../components/Stepcard";

function LandingPage() {

    const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.3 });

    const steps = [
        { img: "images/Step1.png", title: "Step 1", desc: "Upload your resume." },
        { img: "images/Step2.png", title: "Step 2", desc: "Upload your job description." },
        { img: "images/Step3.jpg", title: "Step 3", desc: "Get AI analytics of matching and missing skills." },
        { img: "images/Step4.png", title: "Step 4", desc: "View your fit score instantly." },
    ];




    return (
        <div className="flex flex-col">

            <nav className="fixed top-0 left-0 w-full bg-zinc-900 bg-opacity-90 text-white shadow-lg z-50 backdrop-blur-md">
                <div className="max-w-6xl mx-auto flex justify-between items-center px-2 py-4">

                    {/* System Name / Brand */}
                    <div className="text-2xl font-extrabold font-serif tracking-wide -ml-6">
                        AI Resume Matcher
                    </div>

                    {/* Nav Links */}
                    <div className="flex space-x-6">
                        <a href="#hero" className="px-4 py-2 rounded-md hover:bg-zinc-800 hover:text-zinc-200 transition-all duration-300">Home</a>
                        <a href="#stats" className="px-4 py-2 rounded-md hover:bg-zinc-800 hover:text-zinc-200 transition-all duration-300">Stats</a>
                        <a href="#how-it-works" className="px-4 py-2 rounded-md hover:bg-zinc-800 hover:text-zinc-200 transition-all duration-300">How It Works</a>
                    </div>

                </div>
            </nav>

            {/*First-sight content */}
            <section id="hero" className="h-screen flex items-center justify-center bg-zinc-900 text-white">
                <div className="flex flex-col w-1/3 justify-center items-start ml-[3%] gap-6">
                    <h1 className="text-3xl font-bold font-sans mb-[2%]">See How Your Resume Measures Up!</h1>
                    <p className="text-lg font-serif">Welcome to the AI Resume Matcher! Upload your resume and job descriptions, and instantly see how well you fit each job. Discover which skills you have, which ones are missing, and get your personalized fit score in seconds.</p>
                    <p className="text-lg font-serif">To get started, click the button below to upload your resume and job descriptions.</p>


                    <Link to="/upload">
                        <button className="bg-zinc-900 border border-white hover:bg-zinc-800 text-white font-bold py-2 px-4 rounded">
                            Get Started
                        </button>
                    </Link>
                </div>

                {/* Image section */}

                <div className="hidden md:flex md:w-2/3 items-center justify-end mr-4">
                    <img
                        src="images/LandingPage1.png"
                        alt="AI Resume Analysis"
                        className="max-w-lg"
                    />
                </div>
            </section>


            {/*Stats Section*/}
            <section
                id="stats"
                ref={ref}
                className="bg-zinc-900 bg-opacity-90 shadow-zinc-950 text-white flex flex-col justify-center items-center px-8 backdrop-blur-md">
                <h2 className="text-3xl md:text-4xl font-bold mb-12">Your Resume at a Glance</h2>
                <div className="flex flex-wrap justify-center gap-18 text-center mb-4">
                    <div className="mr-12">
                        <h3 className="text-5xl md:text-5xl font-bold">
                            {inView ? <CountUp end={100} duration={2} /> : 0}+
                        </h3>
                        <p className="text-lg text-zinc-400">Candidates Matched</p>
                    </div>
                    <div className="mr-12">
                        <h3 className="text-5xl md:text-5xl font-bold">
                            {inView ? <CountUp end={200} duration={2} /> : 0}+
                        </h3>
                        <p className="text-lg text-zinc-400">Skills Matched</p>
                    </div>
                    <div className="mr-12">
                        <h3 className="text-5xl md:text-5xl font-bold">
                            {inView ? <CountUp end={50} duration={2} /> : 0}+
                        </h3>
                        <p className="text-lg text-zinc-400">Missing Skills Highlighted</p>
                    </div>
                    <div className="mr-12">
                        <h3 className="text-5xl md:text-5xl font-bold">
                            {inView ? <CountUp end={5} duration={2} /> : 0}s
                        </h3>
                        <p className="text-lg text-zinc-400">Analysis Time</p>
                    </div>
                </div>
            </section>


            {/*How it works section */}
            <section id="how-it-works" className="bg-zinc-900 text-white flex flex-col py-16">

                <div className="flex flex-col justify-center items-center mt-12">
                    <h2 className="text-3xl font-bold">How it works</h2>
                    <p className="max-w-xl">Our system quickly analyzes your resume and highlights the most important insights. It matches your skills to relevant opportunities, points out gaps to improve, and delivers clear results all in just a few seconds. Think of it as your personal career spotlight, showing you what matters most.</p>
                </div>


                <div className="flex flex-col md:flex-row justify-center items-stretch gap-8 mt-16 px-16">
                    {steps.map((step, index) => (
                        <StepCard key={index} step={step} index={index} />
                    ))}

                </div>

                <div className="flex flex-col items-center text-center mt-12">
                    <Link to="/upload">
                        <button className="bg-zinc-900 border border-white hover:bg-zinc-800 text-white font-bold py-2 px-4 rounded">
                            Get Started
                        </button>
                    </Link>
                </div>

                <div className="flex flex-col items-center text-center mt-24 px-8">
                    <h2 className="text-4xl md:text-5xl font-bold mb-2">Signal, Not Noise</h2>
                    <p className="text-zinc-400 max-w-lg">
                        See clear insights, skip the fluff, and understand exactly where your skills stand.
                    </p>
                </div>





            </section>


        </div>
    );
}

export default LandingPage;