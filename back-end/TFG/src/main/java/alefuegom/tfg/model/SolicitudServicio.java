package alefuegom.tfg.model;

import java.time.LocalDateTime;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import com.sun.istack.NotNull;

@Entity
@Table(name="solicitudServicios")
public class SolicitudServicio extends BaseEntity{
		
	@NotNull
	private EstadoSolicitud estado;
	
	@NotNull
	private LocalDateTime date;
	
	private String observaciones;
	
	@ManyToOne(cascade= CascadeType.ALL)
	private Tratamiento tratamiento;
//	
//	@ManyToOne(cascade= CascadeType.ALL)
//	private Plaga plaga;


	public EstadoSolicitud getEstado() {
		return estado;
	}

	public void setEstado(EstadoSolicitud estado) {
		this.estado = estado;
	}

	public LocalDateTime getDate() {
		return date;
	}

	public void setDate(LocalDateTime date) {
		this.date = date;
	}

	public String getObservaciones() {
		return observaciones;
	}

	public void setObservaciones(String observaciones) {
		this.observaciones = observaciones;
	}
	
	

}
