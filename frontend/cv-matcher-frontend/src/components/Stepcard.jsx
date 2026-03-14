// StepCard.jsx (or at the top of LandingPage.jsx but outside the LandingPage function)
import { useInView } from "react-intersection-observer";
import { motion } from "framer-motion";

export default function StepCard({ step, index }) {
    const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.3 });

    return (
        <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 20 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: index * 0.2 }}
            className="flex flex-col items-center bg-zinc-950 bg-opacity-50 shadow-lg w-60 p-6 h-80 ml-2 hover:scale-105 hover:shadow-2xl transition-transform duration-300"
        >
            <img
                src={step.img}
                alt={step.title}
                className="w-32 h-32 mb-4 object-cover rounded-full"
            />
            <h3 className="text-xl font-bold mb-2">{step.title}</h3>
            <p className="text-center text-gray-300">{step.desc}</p>
        </motion.div>
    );
}