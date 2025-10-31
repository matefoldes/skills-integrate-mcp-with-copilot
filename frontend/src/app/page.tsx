'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';

interface Activity {
  description: string;
  schedule: string;
  max_participants: number;
  participants: string[];
}

interface Activities {
  [key: string]: Activity;
}

export default function Home() {
  const [activities, setActivities] = useState<Activities>({});
  const [loading, setLoading] = useState(true);
  const [email, setEmail] = useState('');
  const [selectedActivity, setSelectedActivity] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('');

  const fetchActivities = async () => {
    try {
      const response = await fetch('/activities');
      const data = await response.json();
      setActivities(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching activities:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchActivities();
  }, []);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(selectedActivity)}/signup?email=${encodeURIComponent(email)}`,
        { method: 'POST' }
      );
      const result = await response.json();

      if (response.ok) {
        setMessage(result.message);
        setMessageType('success');
        setEmail('');
        setSelectedActivity('');
        fetchActivities();
      } else {
        setMessage(result.detail || 'An error occurred');
        setMessageType('error');
      }

      setTimeout(() => {
        setMessage('');
        setMessageType('');
      }, 5000);
    } catch (error) {
      console.error('Error signing up:', error);
      setMessage('Failed to sign up. Please try again.');
      setMessageType('error');
    }
  };

  const handleUnregister = async (activityName: string, participantEmail: string) => {
    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activityName)}/unregister?email=${encodeURIComponent(participantEmail)}`,
        { method: 'DELETE' }
      );
      const result = await response.json();

      if (response.ok) {
        setMessage(result.message);
        setMessageType('success');
        fetchActivities();
      } else {
        setMessage(result.detail || 'An error occurred');
        setMessageType('error');
      }

      setTimeout(() => {
        setMessage('');
        setMessageType('');
      }, 5000);
    } catch (error) {
      console.error('Error unregistering:', error);
      setMessage('Failed to unregister. Please try again.');
      setMessageType('error');
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Animated background */}
      <div className="fixed inset-0 -z-10 opacity-[0.08]" 
           style={{
             background: `
               linear-gradient(90deg, transparent 0%, transparent calc(50% - 1px), #32cd32 calc(50% - 1px), #32cd32 calc(50% + 1px), transparent calc(50% + 1px)),
               linear-gradient(45deg, transparent 0%, transparent calc(25% - 1px), #32cd32 calc(25% - 1px), #32cd32 calc(25% + 1px), transparent calc(25% + 1px)),
               linear-gradient(-45deg, transparent 0%, transparent calc(75% - 1px), #32cd32 calc(75% - 1px), #32cd32 calc(75% + 1px), transparent calc(75% + 1px))
             `,
             backgroundSize: '200px 200px, 300px 300px, 300px 300px',
             animation: 'branchFlow 20s linear infinite'
           }}>
      </div>

      {/* Header */}
      <header className="bg-[#32cd32] text-white text-center py-8 mb-8 rounded-lg shadow-lg mx-4 mt-4">
        <h1 className="text-4xl font-bold mb-2">Mergington High School</h1>
        <h2 className="text-2xl mb-4">Extracurricular Activities</h2>
        <div className="flex justify-center gap-5 mt-4">
          <Image src="https://octodex.github.com/images/original.png" alt="Octocat Mascot" width={60} height={60} className="drop-shadow-lg" />
          <Image src="https://octodex.github.com/images/hulatocat.png" alt="Hulatocat Mascot" width={60} height={60} className="drop-shadow-lg" />
          <Image src="https://octodex.github.com/images/adventure-cat.png" alt="Adventure Cat Mascot" width={60} height={60} className="drop-shadow-lg" />
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 pb-8">
        <div className="flex flex-wrap gap-8 justify-center">
          {/* Activities List */}
          <section className="bg-white rounded-lg shadow-md p-6 w-full max-w-[500px]">
            <h3 className="text-2xl mb-5 pb-2 border-b-2 border-[#32cd32] text-[#32cd32]">
              Available Activities
            </h3>
            {loading ? (
              <p>Loading activities...</p>
            ) : (
              <div className="space-y-4">
                {Object.entries(activities).map(([name, details]) => {
                  const spotsLeft = details.max_participants - details.participants.length;
                  return (
                    <div key={name} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                      <h4 className="text-xl font-semibold text-[#32cd32] mb-2">{name}</h4>
                      <p className="mb-2">{details.description}</p>
                      <p className="mb-2">
                        <strong>Schedule:</strong> {details.schedule}
                      </p>
                      <p className="mb-3">
                        <strong>Availability:</strong> {spotsLeft} spots left
                      </p>
                      <div className="mt-3 pt-3 border-t border-dashed border-gray-300">
                        {details.participants.length > 0 ? (
                          <div>
                            <h5 className="text-[#32cd32] font-semibold mb-2">Participants:</h5>
                            <ul className="space-y-1">
                              {details.participants.map((participant, idx) => (
                                <li key={idx} className="flex justify-between items-center">
                                  <span className="flex-grow">{participant}</span>
                                  <button
                                    onClick={() => handleUnregister(name, participant)}
                                    className="text-red-700 hover:bg-red-50 rounded px-2 py-1 transition-colors"
                                  >
                                    ❌
                                  </button>
                                </li>
                              ))}
                            </ul>
                          </div>
                        ) : (
                          <p className="text-gray-500 italic">No participants yet</p>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </section>

          {/* Signup Form */}
          <section className="bg-white rounded-lg shadow-md p-6 w-full max-w-[500px]">
            <h3 className="text-2xl mb-5 pb-2 border-b-2 border-[#32cd32] text-[#32cd32]">
              Sign Up for an Activity
            </h3>
            <form onSubmit={handleSignup} className="space-y-4">
              <div>
                <label htmlFor="email" className="block font-bold mb-2">
                  Student Email:
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="your-email@mergington.edu"
                  className="w-full px-3 py-2 border border-gray-300 rounded text-base"
                />
              </div>
              <div>
                <label htmlFor="activity" className="block font-bold mb-2">
                  Select Activity:
                </label>
                <select
                  id="activity"
                  value={selectedActivity}
                  onChange={(e) => setSelectedActivity(e.target.value)}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded text-base"
                >
                  <option value="">-- Select an activity --</option>
                  {Object.keys(activities).map((name) => (
                    <option key={name} value={name}>
                      {name}
                    </option>
                  ))}
                </select>
              </div>
              <button
                type="submit"
                className="bg-[#32cd32] text-white px-4 py-2 rounded text-base hover:bg-[#28a428] transition-colors w-full"
              >
                Sign Up
              </button>
            </form>
            {message && (
              <div
                className={`mt-5 p-3 rounded ${
                  messageType === 'success'
                    ? 'bg-green-50 text-green-800 border border-green-200'
                    : 'bg-red-50 text-red-800 border border-red-200'
                }`}
              >
                {message}
              </div>
            )}
          </section>
        </div>

        {/* Mascots Gallery */}
        <section className="bg-white rounded-lg shadow-md p-8 mt-8">
          <h3 className="text-2xl text-center mb-6 pb-2 border-b-2 border-[#32cd32] text-[#32cd32]">
            Our Mascots
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-5 justify-items-center">
            <Image
              src="https://octodex.github.com/images/octocat-de-los-muertos.jpg"
              alt="Octocat de los Muertos"
              width={150}
              height={150}
              className="transition-transform hover:scale-110 cursor-pointer"
            />
            <Image
              src="https://octodex.github.com/images/daftpunktocat-guy.gif"
              alt="Daft Punk Octocat"
              width={150}
              height={150}
              className="transition-transform hover:scale-110 cursor-pointer"
            />
            <Image
              src="https://octodex.github.com/images/Professortocat_v2.png"
              alt="Professor Octocat"
              width={150}
              height={150}
              className="transition-transform hover:scale-110 cursor-pointer"
            />
            <Image
              src="https://octodex.github.com/images/stormtroopocat.png"
              alt="Stormtrooper Octocat"
              width={150}
              height={150}
              className="transition-transform hover:scale-110 cursor-pointer"
            />
            <Image
              src="https://octodex.github.com/images/jetpacktocat.png"
              alt="Jetpack Octocat"
              width={150}
              height={150}
              className="transition-transform hover:scale-110 cursor-pointer"
            />
            <Image
              src="https://octodex.github.com/images/total-eclipse-of-the-octocat.jpg"
              alt="Eclipse Octocat"
              width={150}
              height={150}
              className="transition-transform hover:scale-110 cursor-pointer"
            />
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="text-center mt-8 py-5 text-gray-600">
        <p>&copy; 2023 Mergington High School</p>
      </footer>

      <style jsx>{`
        @keyframes branchFlow {
          0% {
            background-position: 0 0, 0 0, 0 0;
          }
          100% {
            background-position: 200px 0, 300px 300px, -300px 300px;
          }
        }
      `}</style>
    </div>
  );
}
