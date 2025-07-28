export default function Footer() {
  return (
    <footer className="bg-primary text-purple/60 py-4 text-center text-sm w-full border-t border-yellow-900">
      © {new Date().getFullYear()} UVic Course Planner
    </footer>
  );
}