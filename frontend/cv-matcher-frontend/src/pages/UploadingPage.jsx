import { useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";


export default function UploadingPage() {

    const [resume, setResume] = useState(null);
    const [jobDescription, setJobDescription] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const navigate = useNavigate();

    const handleSubmit = async () => {
        if (!resume || !jobDescription) {
            setError("Please upload a resume and enter a job description.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append("cv_file", resume);
            formData.append("job_description", jobDescription);

            const response = await fetch("https://cv-matching-system-7o0r.onrender.com/match", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Failed to analyze resume. Please try again.");
            }

            const result = await response.json();
            console.log("Backend response: " + JSON.stringify(result));

            navigate("/results", { state: { result } })
        } catch (err) {
            console.error(err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className="min-h-screen bg-zinc-900 text-white flex flex-col p-10">

            <nav className="fixed top-0 left-0 w-full bg-zinc-900 bg-opacity-90 text-white shadow-lg z-50 backdrop-blur-md">
                <div className="max-w-6xl mx-auto flex justify-between items-center px-2 py-6">

                    {/* System Name / Brand */}
                    <div className="text-2xl font-extrabold font-serif tracking-wide -ml-6">
                        AI Resume Matcher
                    </div>
                </div>
            </nav>



            <div className="flex flex-row items-start justify-start mt-20">
                <Link to="/" className=" text-zinc-400 hover:text-zinc-100 transition">
                    back
                </Link>
            </div>

            <div className="flex flex-col items-center justify-center mt-10">

                <h1 className="text-4xl font-bold mb-10">
                    Upload & Analyze Resume
                </h1>

                <div className="flex gap-10 w-full max-w-6xl">

                    {/* CV Upload */}
                    <div className="flex flex-col w-1/2 bg-zinc-800 p-8 rounded-xl border border-zinc-700">

                        <h2 className="text-2xl font-semibold mb-6">
                            Drop Your CV
                        </h2>

                        <label className="flex flex-col items-center justify-center border-2 border-dashed border-zinc-600 rounded-lg h-64 cursor-pointer hover:border-zinc-300 transition">

                            <input
                                type="file"
                                accept=".pdf,.doc,.docx"
                                className="hidden"
                                onChange={(e) => setResume(e.target.files[0])}
                            />

                            <p className="text-zinc-400">
                                Drag & drop your CV here
                            </p>

                            <p className="text-sm text-zinc-500 mt-2">
                                or click to upload
                            </p>

                            {resume && (
                                <p className="mt-4 text-white font-semibold">
                                    {resume.name}
                                </p>
                            )}

                        </label>

                    </div>

                    {/* Job Description */}
                    <div className="flex flex-col w-1/2 bg-zinc-800 p-8 rounded-xl border border-zinc-700">

                        <h2 className="text-2xl font-semibold mb-6">
                            Paste Job Description
                        </h2>

                        <textarea
                            value={jobDescription}
                            onChange={(e) => setJobDescription(e.target.value)}
                            placeholder="Paste the job description here..."
                            className="h-64 bg-zinc-900 border border-zinc-700 rounded-lg p-4 text-white resize-none focus:outline-none focus:border-zinc-300"
                        />

                    </div>

                </div>

                {/* Analyze Button */}

                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="mt-10 bg-zinc-900 border border-white hover:bg-zinc-700 text-white px-10 py-3 rounded-lg font-bold transition">
                    {loading ? "Analyzing..." : "Analyze Resume"}
                </button>
                {error && <p className="text-red-500 mt-4">{error} </p>}


            </div>



        </div>
    );
}
