from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from joblib import dump, load
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression

from users.models import CustomUser
from school.models import Grade, Enrollment

MODEL_PATH = Path(settings.BASE_DIR) / 'ml_model.joblib'

@login_required
def train_model(request):
    if request.user.role not in [CustomUser.Role.ADMIN, CustomUser.Role.TEACHER]:
        messages.error(request, 'Only Admin/Teacher can train the model.')
        return redirect('dashboard')

    X, y = [], []
    students = CustomUser.objects.filter(role=CustomUser.Role.STUDENT)
    for s in students:
        enrolls = Enrollment.objects.filter(student=s)
        scores = list(Grade.objects.filter(enrollment__in=enrolls).values_list('score', flat=True))
        if scores:
            avg = float(np.mean(scores))
            X.append([avg])
            y.append(1 if avg < 60 else 0)

    if len(X) < 10:
        synth_scores = np.linspace(30, 95, 40)
        for sc in synth_scores:
            X.append([float(sc)])
            y.append(1 if sc < 60 else 0)

    model = LogisticRegression()
    model.fit(np.array(X), np.array(y))
    dump(model, MODEL_PATH)
    messages.success(request, f'Model trained on {len(X)} samples. Saved to {MODEL_PATH.name}.')
    return redirect('dashboard')

@login_required
def predict_student(request, student_id: int):
    student = get_object_or_404(CustomUser, pk=student_id, role=CustomUser.Role.STUDENT)
    if request.user.role not in [CustomUser.Role.ADMIN, CustomUser.Role.TEACHER] and request.user.id != student.id:
        messages.error(request, 'Permission denied for prediction.')
        return redirect('dashboard')

    if not MODEL_PATH.exists():
        messages.error(request, 'Model not trained yet. Train it from the Admin/Teacher dashboard.')
        return redirect('student_detail', user_id=student.id)

    model = load(MODEL_PATH)

    enrolls = Enrollment.objects.filter(student=student)
    scores = list(Grade.objects.filter(enrollment__in=enrolls).values_list('score', flat=True))
    avg = float(np.mean(scores)) if scores else 50.0
    if not scores:
        messages.warning(request, 'No grades for this student yet; prediction may be less meaningful.')

    proba = float(model.predict_proba(np.array([[avg]]))[0][1])
    is_risky = proba >= 0.5
    messages.info(request, f"Predicted risk for {student.username}: {'AT-RISK' if is_risky else 'OK'} (p={proba:.2f}, avg={avg:.1f}).")
    return redirect('student_detail', user_id=student.id)
