import { useState } from "react";

function App() {
  const [formData, setFormData] = useState({
    age: "",
    sex: "",
    cp: "",
    trestbps: "",
    chol: "",
    fbs: "",
    restecg: "",
    thalach: "",
    exang: "",
    oldpeak: "",
    slope: "",
    ca: "",
    thal: ""
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setPrediction(null);

    if (Object.values(formData).some((value) => value === "")) {
      setError("Please fill in all fields before submitting.");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          age: Number(formData.age),
          sex: Number(formData.sex),
          cp: Number(formData.cp),
          trestbps: Number(formData.trestbps),
          chol: Number(formData.chol),
          fbs: Number(formData.fbs),
          restecg: Number(formData.restecg),
          thalach: Number(formData.thalach),
          exang: Number(formData.exang),
          oldpeak: Number(formData.oldpeak),
          slope: Number(formData.slope),
          ca: Number(formData.ca),
          thal: Number(formData.thal)
        })
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.detail || "The prediction request failed."
        );
      }

      setPrediction(result);
    } catch (requestError) {
      setError(
        requestError.message ||
        "Could not connect to the prediction API."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const inputClass =
    "mt-2 w-full rounded-lg border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100";

  const labelClass =
    "text-sm font-medium text-slate-700";

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="mx-auto max-w-5xl">

        {/* HEADER */}
        <div className="mb-8 text-center">
          <div className="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-600 text-2xl text-white shadow-lg">
            ♥
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Heart Disease Prediction
          </h1>

          <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
            Enter the patient's health information below to generate
            a machine-learning prediction.
          </p>
        </div>

        {/* MAIN CARD */}
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">

          {/* CARD HEADER */}
          <div className="border-b border-slate-200 px-6 py-5 sm:px-8">
            <h2 className="text-lg font-semibold text-slate-900">
              Patient Information
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Provide all required measurements and clinical information.
            </p>
          </div>

          {/* FORM */}
          <form onSubmit={handleSubmit} className="px-6 py-7 sm:px-8">

            {/* BASIC INFORMATION */}
            <div className="mb-8">
              <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-500">
                Basic Information
              </h3>

              <div className="grid gap-5 sm:grid-cols-2">

                {/* AGE */}
                <div>
                  <label htmlFor="age" className={labelClass}>
                    Age
                  </label>

                  <input
                    id="age"
                    type="number"
                    name="age"
                    value={formData.age}
                    onChange={handleChange}
                    min="1"
                    max="120"
                    placeholder="e.g. 55"
                    className={inputClass}
                  />
                </div>

                {/* SEX */}
                <div>
                  <label htmlFor="sex" className={labelClass}>
                    Sex
                  </label>

                  <select
                    id="sex"
                    name="sex"
                    value={formData.sex}
                    onChange={handleChange}
                    className={inputClass}
                  >
                    <option value="">Select sex</option>
                    <option value="0">Female</option>
                    <option value="1">Male</option>
                  </select>
                </div>

              </div>
            </div>

            {/* CARDIOVASCULAR INFORMATION */}
            <div className="mb-8">
              <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-500">
                Cardiovascular Information
              </h3>

              <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">

                {/* CHEST PAIN */}
                <div>
                  <label htmlFor="cp" className={labelClass}>
                    Chest Pain Type
                  </label>

                  <select
                    id="cp"
                    name="cp"
                    value={formData.cp}
                    onChange={handleChange}
                    className={inputClass}
                  >
                    <option value="">Select type</option>
                    <option value="0">Typical Angina</option>
                    <option value="1">Atypical Angina</option>
                    <option value="2">Non-Anginal Pain</option>
                    <option value="3">Asymptomatic</option>
                  </select>
                </div>

                {/* BLOOD PRESSURE */}
                <div>
                  <label htmlFor="trestbps" className={labelClass}>
                    Resting Blood Pressure
                  </label>

                  <input
                    id="trestbps"
                    type="number"
                    name="trestbps"
                    value={formData.trestbps}
                    onChange={handleChange}
                    placeholder="e.g. 130"
                    min="50"
                    max="250"
                    className={inputClass}
                  />
                </div>

                {/* CHOLESTEROL */}
                <div>
                  <label htmlFor="chol" className={labelClass}>
                    Cholesterol
                  </label>

                  <input
                    id="chol"
                    type="number"
                    name="chol"
                    value={formData.chol}
                    onChange={handleChange}
                    placeholder="e.g. 240"
                    min="50"
                    max="700"
                    className={inputClass}
                  />
                </div>

                {/* FASTING BLOOD SUGAR */}
                <div>
                  <label htmlFor="fbs" className={labelClass}>
                    Fasting Blood Sugar
                  </label>

                  <select
                    id="fbs"
                    name="fbs"
                    value={formData.fbs}
                    onChange={handleChange}
                    className={inputClass}
                  >
                    <option value="">Select option</option>
                    <option value="0">No (≤ 120 mg/dl)</option>
                    <option value="1">Yes (&gt; 120 mg/dl)</option>
                  </select>
                </div>

                {/* RESTING ECG */}
                <div>
                  <label htmlFor="restecg" className={labelClass}>
                    Resting ECG
                  </label>

                  <select
                    id="restecg"
                    name="restecg"
                    value={formData.restecg}
                    onChange={handleChange}
                    className={inputClass}
                  >
                    <option value="">Select result</option>
                    <option value="0">Normal</option>
                    <option value="1">ST-T Wave Abnormality</option>
                    <option value="2">
                      Left Ventricular Hypertrophy
                    </option>
                  </select>
                </div>

                {/* MAX HEART RATE */}
                <div>
                  <label htmlFor="thalach" className={labelClass}>
                    Maximum Heart Rate
                  </label>

                  <input
                    id="thalach"
                    type="number"
                    name="thalach"
                    value={formData.thalach}
                    onChange={handleChange}
                    placeholder="e.g. 150"
                    min="50"
                    max="250"
                    className={inputClass}
                  />
                </div>

              </div>
            </div>

            {/* TEST RESULTS */}
            <div className="mb-8">
              <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-500">
                Test Results
              </h3>

              <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">

                {/* EXERCISE ANGINA */}
                <div>
                  <label htmlFor="exang" className={labelClass}>
                    Exercise-Induced Angina
                  </label>

                  <select
                    id="exang"
                    name="exang"
                    value={formData.exang}
                    onChange={handleChange}
                    className={inputClass}
                  >
                    <option value="">Select option</option>
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                  </select>
                </div>

                {/* OLDPEAK */}
                <div>
                  <label htmlFor="oldpeak" className={labelClass}>
                    Oldpeak
                  </label>

                  <input
                    id="oldpeak"
                    type="number"
                    step="0.1"
                    name="oldpeak"
                    value={formData.oldpeak}
                    onChange={handleChange}
                    placeholder="e.g. 1.5"
                    min="0"
                    max="10"
                    className={inputClass}
                  />
                </div>

                {/* SLOPE */}
                <div>
                  <label htmlFor="slope" className={labelClass}>
                    ST Segment Slope
                  </label>

                  <select
                    id="slope"
                    name="slope"
                    value={formData.slope}
                    onChange={handleChange}
                    className={inputClass}
                  >
                    <option value="">Select slope</option>
                    <option value="0">Upsloping</option>
                    <option value="1">Flat</option>
                    <option value="2">Downsloping</option>
                  </select>
                </div>

                {/* CA */}
                <div>
                  <label htmlFor="ca" className={labelClass}>
                    Major Vessels
                  </label>

                  <select
                    id="ca"
                    name="ca"
                    value={formData.ca}
                    onChange={handleChange}
                    className={inputClass}
                  >
                    <option value="">Select number</option>
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                  </select>
                </div>

                {/* THAL */}
                <div>
                  <label htmlFor="thal" className={labelClass}>
                    Thalassemia
                  </label>

                  <select
                    id="thal"
                    name="thal"
                    value={formData.thal}
                    onChange={handleChange}
                    className={inputClass}
                  >
                    <option value="">Select type</option>
                    <option value="0">Normal</option>
                    <option value="1">Fixed Defect</option>
                    <option value="2">Reversible Defect</option>
                  </select>
                </div>

              </div>
            </div>

            {/* ERROR */}
            {error && (
              <div
                role="alert"
                className="mb-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
              >
                {error}
              </div>
            )}

            {/* SUBMIT */}
            <div className="border-t border-slate-200 pt-6">
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full rounded-lg bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
              >
                {isSubmitting ? "Generating Prediction..." : "Predict Heart Disease"}
              </button>
            </div>

          </form>
        </div>

        {/* PREDICTION RESULT */}
        {prediction !== null && (
          <div className="mt-6 overflow-hidden rounded-2xl border border-blue-200 bg-white shadow-sm">
            <div className="border-l-4 border-blue-600 p-6">
              <p className="text-sm font-medium uppercase tracking-wider text-blue-600">
                Prediction Result
              </p>

              <h2 className="mt-2 text-2xl font-bold text-slate-900">
                {prediction.message}
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                This result was generated by the trained machine-learning model.
              </p>
            </div>
          </div>
        )}

        {/* DISCLAIMER */}
        <p className="mx-auto mt-6 max-w-3xl text-center text-xs leading-5 text-slate-400">
          This application is for educational and demonstration purposes only.
          The prediction should not be used as a medical diagnosis or as a
          substitute for professional medical advice.
        </p>

      </div>
    </div>
  );
}

export default App;
