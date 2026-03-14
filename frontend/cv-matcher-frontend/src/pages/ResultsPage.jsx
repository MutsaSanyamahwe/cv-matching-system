import { useLocation, useNavigate } from "react-router-dom";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { useState } from "react";
import { Link } from "react-router-dom";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function ResultsPage() {
    const { state } = useLocation();
    const navigate = useNavigate();
    const result = state?.result;

    const [showAllMatched, setShowAllMatched] = useState(false);
    const [showAllMissing, setShowAllMissing] = useState(false);

    if (!result) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-900 text-white">
                <p className="text-xl">No results to display.</p>
                <button
                    onClick={() => navigate("/upload")}
                    className="mt-4 bg-indigo-600 px-6 py-2 rounded-lg hover:bg-indigo-500 transition"
                >
                    Upload Resume
                </button>
            </div>
        );
    }

    const { fit_score, matched_skills, missing_skills } = result;

    const coverageData = {
        labels: ["Matched Skills", "Missing Skills"],
        datasets: [
            {
                data: [matched_skills.length, missing_skills.length],
                backgroundColor: ["#6366F1", "#0D9488"],
                borderWidth: 2,
            },
        ],
    };

    return (
        <div className="min-h-screen bg-zinc-900 text-white">
            {/* Navbar */}
            <nav className="fixed top-0 left-0 w-full bg-zinc-900/70 backdrop-blur-md text-white shadow-md z-50">
                <div className="max-w-6xl mx-auto flex justify-between items-center px-6 py-4">
                    <div className="text-2xl font-bold tracking-wide text-white">
                        AI Resume Matcher
                    </div>
                </div>
            </nav>



            <main className="max-w-6xl mx-auto px-6 pt-8 pb-16 space-y-12">

                <div className="flex flex-row items-start justify-start mt-8 pt-12">
                    <Link to="/upload" className=" text-zinc-400 hover:text-zinc-100 transition">
                        back
                    </Link>
                </div>


                {/* Header */}
                <div className="text-center mt-0">
                    <h1 className="text-4xl font-bold mb-2">Your Results</h1>
                    <p className="text-zinc-400">An overview of your resume fit</p>
                </div>

                {/* Fit Score + Skills Coverage */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Fit Score */}
                    <div className="bg-zinc-800/60 backdrop-blur-md p-6 rounded-xl border border-zinc-700 flex flex-col items-center">
                        <h2 className="text-3xl font-extrabold text-indigo-400">{fit_score}%</h2>
                        <p className="text-zinc-400 mt-1 text-sm">Candidate Fit Score</p>

                        {/* Circular Gauge */}
                        <div className="relative w-24 h-24 mt-6">
                            <svg className="w-full h-full">
                                <circle className="text-zinc-700" strokeWidth="6" stroke="currentColor" fill="transparent" r="40" cx="50" cy="50" />
                                <circle
                                    className="text-indigo-400"
                                    strokeWidth="6"
                                    strokeDasharray={2 * Math.PI * 40}
                                    strokeDashoffset={2 * Math.PI * 40 - (fit_score / 100) * 2 * Math.PI * 40}
                                    strokeLinecap="round"
                                    stroke="currentColor"
                                    fill="transparent"
                                    r="40"
                                    cx="50"
                                    cy="50"
                                />
                            </svg>
                            <span className="absolute inset-0 flex items-center justify-center text-lg font-bold">
                                {fit_score}%
                            </span>
                        </div>

                        {/* Status Label */}
                        <p className="mt-3 text-sm font-semibold text-indigo-300">
                            {fit_score > 70 ? "Excellent Fit" : fit_score > 40 ? "Moderate Fit" : "Needs Improvement"}
                        </p>
                    </div>

                    {/* Skills Coverage Chart */}
                    <div className="bg-zinc-800/60 backdrop-blur-md p-6 rounded-xl border border-zinc-700 flex flex-col items-center">
                        <h3 className="text-xl font-bold mb-4">Skills Coverage</h3>
                        <div className="w-48 h-48">
                            <Pie data={coverageData} />
                        </div>
                    </div>
                </div>

                {/* Skills Sections */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Matched Skills */}
                    <div className="bg-zinc-800/60 backdrop-blur-md p-6 rounded-xl border border-zinc-700">
                        <h3 className="text-xl font-bold mb-2">Matched Skills</h3>
                        <p className="text-zinc-400 mb-4 text-sm">{matched_skills.length} skills matched</p>

                        <div
                            className={"flex flex-wrap gap-2 transition-all duration-500"}
                        >
                            {(showAllMatched ? matched_skills : matched_skills.slice(0, 10)).map((skill, idx) => (
                                <span
                                    key={idx}
                                    className="bg-linear-to-r from-indigo-500 to-indigo-600 px-3 py-1 rounded-full text-sm flex items-center gap-1 hover:scale-105 transition"
                                >
                                    {skill}
                                </span>
                            ))}
                        </div>

                        {matched_skills.length > 10 && (
                            <button
                                onClick={() => setShowAllMatched(!showAllMatched)}
                                className="mt-4 text-indigo-400 hover:text-indigo-300 text-sm"
                            >
                                {showAllMatched ? "View Less" : "View More"}
                            </button>
                        )}
                    </div>

                    {/* Missing Skills */}
                    <div className="bg-zinc-800/60 backdrop-blur-md p-6 rounded-xl border border-zinc-700">
                        <h3 className="text-xl font-bold mb-2">Missing Skills</h3>
                        <p className="text-zinc-400 mb-4 text-sm">{missing_skills.length} skills missing</p>

                        <div
                            className="flex flex-wrap gap-2"
                        >
                            {(showAllMissing ? missing_skills : missing_skills.slice(0, 10)).map((skill, idx) => (
                                <span
                                    key={idx}
                                    className="bg-gradient-to-r from-teal-600 to-teal-700 px-3 py-1 rounded-full text-sm flex items-center gap-1 hover:scale-105 transition"
                                >
                                    {skill}
                                </span>
                            ))}
                        </div>

                        {missing_skills.length > 10 && (
                            <button
                                onClick={() => setShowAllMissing(!showAllMissing)}
                                className="mr-24 mt-4 text-indigo-400 hover:text-indigo-300 text-sm"
                            >
                                {showAllMissing ? "View Less" : "View More"}
                            </button>
                        )}

                        {/* CTA */}
                        <button
                            onClick={() => window.open("https://www.coursera.org", "_blank")}
                            className="ml-32 mt-6 bg-transparent border border-white text-white px-4 py-2 rounded-lg hover:bg-zinc-700 transition text-sm"
                        >
                            Learn These Skills
                        </button>


                    </div>
                </div>

                {/* Key Insights */}
                <div className="bg-zinc-800/60 backdrop-blur-md p-8 rounded-xl border border-zinc-700">
                    <h3 className="text-2xl font-bold mb-4">Key Insights</h3>
                    <ul className="list-disc list-inside space-y-2 text-zinc-300">
                        <li>You have strong skills in {matched_skills.slice(0, 5).join(", ")}</li>
                        <li>Consider improving on {missing_skills.slice(0, 5).join(", ")}</li>
                    </ul>
                </div>

                {/* Suggestions */}
                <div className="bg-zinc-800/60 backdrop-blur-md p-6 rounded-xl border border-zinc-700">
                    <h3 className="text-2xl font-bold mb-4">Suggestions to Improve</h3>

                    <ul className="flex flex-col gap-2">
                        {missing_skills.slice(0, 10).map((skill, idx) => (
                            <li
                                key={idx}
                                className="flex items-center gap-2 bg-zinc-800 px-3 py-2 rounded-lg text-sm hover:bg-zinc-600 transition"
                            >
                                <span>Learn or gain experience in {skill}</span>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4 justify-center">
                    <button
                        onClick={() => navigate("/upload")}
                        className="bg-transparent border border-white text-white px-6 py-3 rounded-lg hover:bg-zinc-700 hover:scale-105 transition"
                    >
                        Try Another CV
                    </button>
                    <button
                        onClick={() => navigate("/upload")}
                        className="bg-transparent border border-white text-white px-6 py-3 rounded-lg hover:bg-zinc-700 hover:scale-105 transition"
                    >
                        Try Another Job
                    </button>
                </div>
            </main>
        </div>
    );
}