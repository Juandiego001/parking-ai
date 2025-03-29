import cv2


def do_detection(frame, results, placas_detectadas, threshold=0.4):

    for i, result in enumerate(results.boxes.data.tolist()):
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            if class_id == 0:
                class_id = "Matricula"
            else:
                class_id = "Fondo"

            print('Coordenadas de la BB: ', x1, y1, x2, y2)
            print('Confianza: ', score)
            print('Etiqueta: ', class_id)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)

            placa_texto = placas_detectadas

            if placas_detectadas:
                cv2.putText(frame, f"{class_id}: {placa_texto[0][0][0]}", (
                    x1, y1-45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 5, cv2.LINE_AA)
                cv2.putText(frame, f"Confianza: {placa_texto[0][0][1]:.3f}", (
                    x1, y1-10), cv2.FONT_ITALIC, 0.9, (0, 0, 0), 5, cv2.LINE_AA)
                cv2.putText(frame, f"{class_id}: {placa_texto[0][0][0]}", (
                    x1, y1-45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, f"Confianza: {placa_texto[0][0][1]:.3f}", (
                    x1, y1-10), cv2.FONT_ITALIC, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, f"{class_id} Placa No detectada", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (223, 21, 21), 2, cv2.LINE_AA)

    return frame
