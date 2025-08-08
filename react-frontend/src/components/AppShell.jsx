// components/AppShell.jsx
import Footer from './Footer';
import Header from './Header';
import PublicHeader from './PublicHeader';

export default function AppShell({ children, publicHeader = false }) {
  return (
    <div className="min-h-dvh flex flex-col bg-offwhite">
      {publicHeader ? <PublicHeader /> : <Header />}
      <main className="flex-1 pt-20">{children}</main>
      <Footer />
    </div>
  );
}
